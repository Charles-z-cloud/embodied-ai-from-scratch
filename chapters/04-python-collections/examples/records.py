blocks = [
    {"color": "red", "x_cm": 2.0},
    {"color": "green", "x_cm": 8.0},
    {"color": "red", "x_cm": 7.0},
    {"color": "red", "x_cm": 9.0},
]
red_count = 0
selected = []
for block in blocks:
    if block["color"] == "red":
        red_count = red_count + 1
        if block["x_cm"] > 5.0:
            selected.append(block)
print("红色物体数量：", red_count)
for block in selected:
    print("符合条件的位置：", block["x_cm"])
