def displacement(start_cm, end_cm):
    return end_cm - start_cm


def average_velocity(start_cm, end_cm, duration_s):
    if duration_s <= 0:
        return None
    return displacement(start_cm, end_cm) / duration_s


def select_color(records, color="red"):
    selected = []
    for record in records:
        if record["color"] == color:
            selected.append(record)
    return selected
