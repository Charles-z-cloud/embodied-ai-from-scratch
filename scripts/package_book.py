"""Build a source-only book archive and per-file SHA-256 manifest."""
import hashlib
import json
import zipfile
from check_book import ROOT,publishable_files,main as check

def main():
    check()
    files=publishable_files()
    entries={str(p.relative_to(ROOT)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
    manifest={'edition':'v1.0','content':'Chinese beginner textbook; source, figures and validation records; no generated checkpoints or virtual environment','files':entries}
    manifest_path=ROOT/'release-manifest.json';manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    target=ROOT.parent/'embodied-ai-textbook-v1.0.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for p in files+[manifest_path]:archive.write(p,PathPrefix(p))
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:raise RuntimeError('Archive CRC verification failed')
        for relative,info in entries.items():
            data=archive.read('embodied-ai-textbook/'+relative)
            if hashlib.sha256(data).hexdigest()!=info['sha256']:raise RuntimeError('Archive file hash mismatch: '+relative)
    print(json.dumps({'archive':str(target),'bytes':target.stat().st_size,'files_including_manifest':len(entries)+1,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2))

def PathPrefix(path):return 'embodied-ai-textbook/'+str(path.relative_to(ROOT))
if __name__=='__main__':main()
