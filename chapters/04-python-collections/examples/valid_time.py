duration_s = float(input("请输入经过时间（秒）："))
if duration_s > 0:
    print("平均速度（厘米/秒）：", 6.0 / duration_s)
else:
    print("经过时间必须大于0。")
