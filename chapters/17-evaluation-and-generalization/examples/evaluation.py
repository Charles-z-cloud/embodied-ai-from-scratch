import numpy as np


def remember_and_predict(train_groups, train_labels, query_groups):
    memory = {}
    for group in np.unique(train_groups):
        values = train_labels[train_groups == group]
        memory[int(group)] = int(np.bincount(values, minlength=2).argmax())
    fallback = int(np.bincount(train_labels, minlength=2).argmax())
    return np.array([memory.get(int(group), fallback) for group in query_groups])


def grouped_bootstrap(correct, groups, seed=123, repeats=2000):
    unique = np.unique(groups)
    per_group = np.array([correct[groups == group].mean() for group in unique])
    rng = np.random.default_rng(seed)
    estimates = rng.choice(per_group, size=(repeats, len(per_group)), replace=True).mean(axis=1)
    return np.quantile(estimates, [0.025, 0.975])


def experiment(seed):
    rng = np.random.default_rng(seed)
    labels_by_group = rng.integers(0, 2, size=60)
    groups = np.repeat(np.arange(60), 10)
    labels = labels_by_group[groups]
    rows = rng.permutation(len(groups))
    row_train, row_test = rows[:420], rows[420:]
    group_order = rng.permutation(60)
    group_train = np.flatnonzero(np.isin(groups, group_order[:42]))
    group_test = np.flatnonzero(np.isin(groups, group_order[42:]))
    for name, train, test in (("row split", row_train, row_test),
                              ("object split", group_train, group_test)):
        predicted = remember_and_predict(groups[train], labels[train], groups[test])
        correct = predicted == labels[test]
        overlap = np.intersect1d(groups[train], groups[test])
        interval = grouped_bootstrap(correct, groups[test])
        print("seed", seed, name, "accuracy", correct.mean(), "shared_objects", len(overlap),
              "test_objects", len(np.unique(groups[test])), "object_bootstrap_interval", interval)
        if name == "object split":
            assert len(overlap) == 0


if __name__ == "__main__":
    tp, fp, fn, tn = 8, 2, 4, 86
    print("hand metrics:", (tp + tn) / (tp + fp + fn + tn), tp / (tp + fp), tp / (tp + fn))
    for seed in (7, 42, 2026):
        experiment(seed)
