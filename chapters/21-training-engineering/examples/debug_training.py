import torch
from torch import nn


def fit(y):
    torch.manual_seed(7)
    model = nn.Sequential(nn.Linear(2, 16), nn.ReLU(), nn.Linear(16, 1))
    x = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.], [0., 0.]])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03)
    criterion = nn.BCEWithLogitsLoss()
    for _ in range(700):
        optimizer.zero_grad(set_to_none=True)
        loss = criterion(model(x), y)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        return criterion(model(x), y).item(), torch.sigmoid(model(x)).flatten().tolist()


if __name__ == "__main__":
    torch.set_num_threads(1)
    wrong = torch.tensor([[0.], [1.], [1.], [0.], [1.]])
    corrected = torch.tensor([[0.], [1.], [1.], [0.], [0.]])
    wrong_loss, wrong_prob = fit(wrong)
    correct_loss, correct_prob = fit(corrected)
    print("conflicting labels loss / probability:", wrong_loss, wrong_prob)
    print("corrected labels loss / probability:", correct_loss, correct_prob)
    print("conflict lower bound for all five samples:", 2 * torch.log(torch.tensor(2.)).item() / 5)
    assert correct_loss < 0.02 and wrong_loss > 0.27
    torch.manual_seed(2026)
    dropout = nn.Dropout(0.5)
    values = torch.ones(1000)
    dropout.train()
    with torch.no_grad():
        train_a, train_b = dropout(values), dropout(values)
    dropout.eval()
    with torch.no_grad():
        eval_a, eval_b = dropout(values), dropout(values)
    print("train mode equal:", torch.equal(train_a, train_b), "eval mode equal:", torch.equal(eval_a, eval_b))
    assert not torch.equal(train_a, train_b) and torch.equal(eval_a, values)
