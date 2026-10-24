# 一维位置使用厘米，时间使用秒。
start_cm = 2.0
end_cm = 8.0
duration_s = 3.0
color = "红色"
displacement_cm = end_cm - start_cm
velocity_cm_s = displacement_cm / duration_s
print("位移（厘米）：", displacement_cm)
print("平均速度（厘米/秒）：", velocity_cm_s)
print("目标且时间有效：", color == "红色" and duration_s > 0)
print("浮点误差足够小：", abs((0.1 + 0.2) - 0.3) < 0.000001)
