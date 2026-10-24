import csv
import json
import math
from pathlib import Path

FIELDS = ["color", "start_cm", "end_cm", "duration_s"]


def parse_record(row):
    if set(row) != set(FIELDS):
        raise ValueError("字段数量不匹配")
    for name in FIELDS:
        if row[name] is None or row[name].strip() == "":
            raise ValueError(f"字段缺失：{name}")
    color = row["color"].strip()
    if color not in ["red", "green", "blue"]:
        raise ValueError("未知颜色")
    result = {"color": color}
    for name in FIELDS[1:]:
        value = float(row[name])
        if not math.isfinite(value):
            raise ValueError(f"必须是有限值：{name}")
        result[name] = value
    if result["duration_s"] <= 0:
        raise ValueError("经过时间必须大于0")
    result["displacement_cm"] = result["end_cm"] - result["start_cm"]
    result["velocity_cm_s"] = result["displacement_cm"] / result["duration_s"]
    return result


def process(input_path, output_path):
    accepted = []
    rejected = []
    with open(input_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != FIELDS:
            raise ValueError("表头或单位不符合约定")
        for row in reader:
            try:
                accepted.append(parse_record(row))
            except ValueError as error:
                rejected.append({"line": reader.line_num, "reason": str(error)})
    report = {"accepted_count": len(accepted), "rejected_count": len(rejected),
              "records": accepted, "rejected": rejected}
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2, allow_nan=False)
    return report


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    report = process(base_dir / "records.csv", base_dir / "output" / "report.json")
    print("有效：", report["accepted_count"], "拒绝：", report["rejected_count"])
