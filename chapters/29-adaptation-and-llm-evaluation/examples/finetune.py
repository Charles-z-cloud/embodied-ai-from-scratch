import copy
import json
import sys
from pathlib import Path
import torch
from torch import nn
import torch.nn.functional as F
PREVIOUS = Path(__file__).resolve().parents[2] / "28-tiny-language-model" / "examples"
sys.path.insert(0, str(PREVIOUS))
from train_language import TinyLanguageModel, PAD, BOS, EOS

def main():
    torch.set_num_threads(1)
    torch.manual_seed(7)
    path = PREVIOUS / "output/model_context_16.pt"
    if not path.exists():
        raise SystemExit("Run chapter 28 train_language.py first")
    old = torch.load(path, weights_only=True, map_location="cpu")
    vocab = old["vocabulary"] + sorted(set("方向：") - set(old["vocabulary"]))
    ids = {c: i for i, c in enumerate(vocab)}
    model = TinyLanguageModel(len(vocab), 32)
    state = model.state_dict()
    for key, value in old["state"].items():
        if key == "position.table":
            continue
        if key in ("embedding.weight", "head.weight", "head.bias"):
            state[key][:len(old["vocabulary"])] = value
        else:
            state[key] = value
    model.load_state_dict(state)
    splits = json.loads((PREVIOUS / "output/splits.json").read_text())
    def encode(text):
        prefix = [BOS] + [ids[c] for c in text + "方向："]
        answer = [ids[text[-3]], EOS]
        return prefix, answer
    def pack(texts):
        inputs, labels = [], []
        for text in texts:
            prefix, answer = encode(text)
            sequence = prefix + answer
            x = sequence[:-1]
            y = [-100] * (len(prefix)-1) + answer
            inputs.append(x + [PAD]*(32-len(x)))
            labels.append(y + [-100]*(32-len(y)))
        return torch.tensor(inputs), torch.tensor(labels)
    def score(texts):
        model.eval()
        correct, generated = 0, []
        with torch.no_grad():
            for text in texts:
                prefix, answer = encode(text)
                output = []
                for _ in range(3):
                    token = int(model(torch.tensor([prefix+output]))[0,-1].argmax())
                    output.append(token)
                    if token == EOS: break
                correct += output == answer
                generated.append({"instruction":text,"generated":[vocab[i] for i in output]})
        return {"accuracy":correct/len(texts), "count":len(texts),"samples":generated}
    train_x, train_y = pack(splits["train"])
    val_x, val_y = pack(splits["validation"])
    before = score(splits["test"])
    optimizer = torch.optim.Adam(model.parameters(), lr=.001)
    best, best_state, best_step = float("inf"), None, None
    history = []
    for step in range(1,301):
        model.train()
        idx = torch.randint(len(train_x),(32,))
        loss = F.cross_entropy(model(train_x[idx]).flatten(0,1),train_y[idx].flatten())
        optimizer.zero_grad(); loss.backward(); optimizer.step()
        if step%50 == 0:
            model.eval()
            with torch.no_grad():
                value = F.cross_entropy(model(val_x).flatten(0,1),val_y.flatten()).item()
            history.append([step,value])
            if value < best:
                best, best_step, best_state = value, step, copy.deepcopy(model.state_dict())
    model.load_state_dict(best_state)
    after = score(splits["test"])
    # Low-rank update equivalence, not a LoRA training comparison.
    x, w, a, b = torch.randn(5,32), torch.randn(32,32), torch.randn(4,32), torch.randn(32,4)
    assert torch.allclose(x@(w+b@a).T, x@w.T+(x@a.T)@b.T, atol=2e-5)
    report = {"before":before,"after":after,"validation":history,"best_step":best_step,
              "lora_trainable_parameters":a.numel()+b.numel(),"seed":7}
    folder = Path(__file__).resolve().parent/"output";folder.mkdir(exist_ok=True)
    (folder/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    torch.save({"state":model.state_dict(),"vocabulary":vocab,"context":32},folder/"finetuned.pt")
    print("before",before["accuracy"],"after",after["accuracy"],"best_step",best_step,"LoRA params",256)

if __name__ == "__main__": main()
