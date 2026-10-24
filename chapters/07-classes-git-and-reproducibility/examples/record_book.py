import json
import math
from pathlib import Path


class RecordBook:
    def __init__(self, name):
        self.name = name
        self.records = []

    def add(self, x_cm):
        if not math.isfinite(x_cm):
            raise ValueError("位置必须是有限数值")
        self.records.append({"x_cm": x_cm})

    def count(self):
        return len(self.records)

    def snapshot(self):
        result = []
        for record in self.records:
            result.append(record.copy())
        return result


class NonnegativeBook(RecordBook):
    def add(self, x_cm):
        if x_cm < 0:
            raise ValueError("本记录本不接受负位置")
        super().add(x_cm)


class AboveThreshold:
    def __init__(self, threshold_cm):
        self.threshold_cm = threshold_cm

    def __call__(self, x_cm):
        return x_cm > self.threshold_cm


def main():
    base_dir = Path(__file__).resolve().parent
    with open(base_dir / "config.json", encoding="utf-8") as file:
        config = json.load(file)
    book = RecordBook(config["name"])
    check = AboveThreshold(config["threshold_cm"])
    for x_cm in config["positions_cm"]:
        book.add(x_cm)
    print(book.name, "记录数：", book.count())
    for record in book.snapshot():
        print(record["x_cm"], check(record["x_cm"]))


if __name__ == "__main__":
    main()
