"""Check the book's publishable files without running training."""
import ast
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.venv','.git','__pycache__','output'}

def publishable_files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not p.is_symlink() and not EXCLUDED.intersection(p.relative_to(ROOT).parts) and p.name not in {'.DS_Store','release-manifest.json'} and p.suffix not in {'.pyc','.pyo','.zip','.pt','.pth'})

def anchors(txt):
    result=set(re.findall(r'<a id="([^"]+)"',txt));counts={}
    for m in re.finditer(r'^#{1,6}\s+(.+)$',txt,re.M):
        s=m[1].strip().lower()
        s=''.join(c for c in s if c in '-_ ' or not unicodedata.category(c).startswith(('P','S'))).replace(' ','-')
        count=counts.get(s,0);counts[s]=count+1;result.add(s if count==0 else f'{s}-{count}')
    return result

def main():
    files=publishable_files();allowed={p.resolve() for p in files};errors=[];links=0;images=0
    design=(ROOT/'curriculum.md').read_text();matches=list(re.finditer(r'^### 第 (\d+) 章\s+(.+)$',design,re.M))
    numbers=[int(m[1]) for m in matches]
    if numbers!=list(range(1,59)):errors.append('Chapter design sequence is not 01..58')
    folders=[];prerequisites=0
    for i,m in enumerate(matches):
        n=int(m[1]);block=design[m.end():matches[i+1].start() if i+1<len(matches) else len(design)]
        slug=re.search(r'`chapters/([^`/]+)/`',block)[1];folder=ROOT/'chapters'/slug;folders.append(folder)
        for name in ['README.md','exercises.md','solutions.md','validation.md']:
            if not (folder/name).is_file():errors.append(f'Missing chapter file: {slug}/{name}')
        pre=re.search(r'^- \*\*重点前置\*\*：(.+)$',block,re.M)
        if pre:
            for p in re.findall(r'#ch-(\d+)',pre[1]):
                prerequisites+=1
                if int(p)>=n:errors.append(f'Chapter {n} requires later chapter {p}')
    for i,folder in enumerate(folders):
        body=(folder/'README.md').read_text()
        for j in [i-1,i+1]:
            if 0<=j<len(folders) and f'../{folders[j].name}/README.md' not in body:errors.append(f'Navigation missing: {folder.name} -> {folders[j].name}')
    for f in files:
        if f.suffix=='.py':
            try:ast.parse(f.read_text(),filename=str(f))
            except SyntaxError as e:errors.append(str(e))
        if f.suffix!='.md':continue
        txt=f.read_text()
        if txt.count('```')%2:errors.append(f'Unbalanced code fence: {f.relative_to(ROOT)}')
        for m in re.finditer(r'(!?)\[[^\]]*\]\(([^)]+)\)',txt):
            url=m[2]
            if '://' in url or url.startswith('mailto:'):continue
            links+=1;images+=bool(m[1]);path,_,frag=url.partition('#');target=(f.parent/unquote(path)).resolve() if path else f.resolve()
            if target not in allowed:errors.append(f'Unpublished target: {f.relative_to(ROOT)} -> {url}')
            elif frag and target.suffix=='.md' and unquote(frag) not in anchors(target.read_text()):errors.append(f'Unknown anchor: {f.relative_to(ROOT)} -> {url}')
    report={'chapters':len(folders),'publishable_files':len(files),'markdown_files':sum(f.suffix=='.md' for f in files),'python_files':sum(f.suffix=='.py' for f in files),'png_files':sum(f.suffix=='.png' for f in files),'local_links_including_images':links,'image_links':images,'earlier_chapter_prerequisite_links':prerequisites,'errors':errors}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
