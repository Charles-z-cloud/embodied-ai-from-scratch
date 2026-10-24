import numpy as np


def posterior(prior, detection, false_alarm):
    for value in (prior, detection, false_alarm):
        if not np.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("Probabilities must be finite and in [0, 1]")
    evidence = detection * prior + false_alarm * (1 - prior)
    if evidence == 0:
        raise ValueError("Conditioning on alarm is undefined: alarm probability is zero")
    return detection * prior / evidence


def simulate(seed=2026, n=200_000):
    rng = np.random.default_rng(seed)
    obstacle = rng.random(n) < 0.01
    alarm_probability = np.where(obstacle, 0.9, 0.05)
    alarm = rng.random(n) < alarm_probability
    both = np.sum(obstacle & alarm)
    obstacle_count = np.sum(obstacle)
    alarm_count = np.sum(alarm)
    print("seed:", seed, "obstacles:", obstacle_count, "alarms:", alarm_count, "both:", both)
    detection_estimate = both / obstacle_count if obstacle_count else None
    posterior_estimate = both / alarm_count if alarm_count else None
    print("P(alarm | obstacle):", detection_estimate)
    print("P(obstacle | alarm):", posterior_estimate)
    return obstacle_count, alarm_count, both


if __name__ == "__main__":
    print("table posterior:", 90 / 585)
    print("formula posterior:", posterior(0.01, 0.9, 0.05))
    print("prior=0.5 posterior:", posterior(0.5, 0.9, 0.05))
    simulate()
