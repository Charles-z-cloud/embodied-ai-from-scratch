from collections import Counter


def merge_once(tokens, pair):
    output, i = [], 0
    while i < len(tokens):
        if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == pair:
            output.append(tokens[i] + tokens[i + 1])
            i += 2
        else:
            output.append(tokens[i])
            i += 1
    return output


def learn_merges(words, rounds):
    sequences = [list(word) for word in words]
    merges = []
    for _ in range(rounds):
        counts = Counter()
        for tokens in sequences:
            counts.update(zip(tokens, tokens[1:]))
        if not counts:
            break
        pair = sorted(counts, key=lambda p: (-counts[p], p))[0]
        sequences = [merge_once(tokens, pair) for tokens in sequences]
        merges.append(pair)
    return merges, sequences


def tokenize(word, merges):
    tokens = list(word)
    for pair in merges:
        tokens = merge_once(tokens, pair)
    return tokens


if __name__ == "__main__":
    merges, encoded = learn_merges(["low", "low", "lower", "lowest"], 4)
    print("ordered merges:", merges)
    print("training words:", encoded)
    for word in ("low", "lower", "lowest", "lowering"):
        tokens = tokenize(word, merges)
        print(word, "->", tokens)
        assert "".join(tokens) == word
    assert merge_once(list("aaa"), ("a", "a")) == ["aa", "a"]
