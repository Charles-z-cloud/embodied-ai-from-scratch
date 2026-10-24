from motion import average_velocity, select_color


def main():
    records = [
        {"color": "red", "start_cm": 2.0, "end_cm": 8.0, "duration_s": 3.0},
        {"color": "green", "start_cm": 4.0, "end_cm": 1.0, "duration_s": 1.5},
        {"color": "red", "start_cm": 0.0, "end_cm": 1.0, "duration_s": 0.0},
    ]
    for record in select_color(records):
        velocity = average_velocity(record["start_cm"], record["end_cm"], record["duration_s"])
        if velocity is None:
            print("时间无效")
        else:
            print("平均速度（厘米/秒）：", velocity)


if __name__ == "__main__":
    main()
