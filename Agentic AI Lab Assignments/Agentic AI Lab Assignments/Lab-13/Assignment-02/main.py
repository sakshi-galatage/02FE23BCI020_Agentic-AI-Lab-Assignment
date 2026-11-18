
SENSOR_LOG = [
    {"t": 1, "vibration": 1.8, "temp": 61},
    {"t": 2, "vibration": 2.0, "temp": 63},
    {"t": 3, "vibration": 2.9, "temp": 70},
    {"t": 4, "vibration": 3.2, "temp": 72},
    {"t": 5, "vibration": 3.8, "temp": 75}
]

WARNING_VIBRATION = 2.5
ALARM_VIBRATION = 4.5
WARNING_TEMP = 68
ALARM_TEMP = 80


def classify_reading(reading):
    if (reading["vibration"] >= ALARM_VIBRATION
            or reading["temp"] >= ALARM_TEMP):
        return "ALARM"

    if (reading["vibration"] >= WARNING_VIBRATION
            or reading["temp"] >= WARNING_TEMP):
        return "WARNING"

    return "NORMAL"


def mechanical_agent():
    warning_count = 0
    classifications = []

    for reading in SENSOR_LOG:
        condition = classify_reading(reading)
        classifications.append(condition)

        print(
            f"Reading {reading['t']}: "
            f"Vibration={reading['vibration']}, "
            f"Temperature={reading['temp']}°C "
            f"-> {condition}"
        )

        if condition == "WARNING":
            warning_count += 1
        else:
            warning_count = 0

    latest = SENSOR_LOG[-1]

    if "ALARM" in classifications:
        action = "Recommend shutdown for human review"
    elif warning_count >= 3:
        action = "schedule_inspection"
    else:
        action = "continue_monitoring"

    return {
        "consecutive_warnings": warning_count,
        "latest_reading": latest,
        "recommended_action": action,
        "auto_executed": False
    }


if __name__ == "__main__":
    print("=== MECHANICAL TREND MONITORING ===")

    result = mechanical_agent()

    print("\n=== FINAL RESULT ===")
    for key, value in result.items():
        print(f"{key}: {value}")

    assert result["consecutive_warnings"] == 3
    assert result["recommended_action"] == "schedule_inspection"
    assert all(
        classify_reading(r) != "ALARM" for r in SENSOR_LOG
    )

    print("\n=== VERIFICATION ===")
    print("Three consecutive WARNING readings: PASS")
    print("No ALARM threshold reached: PASS")
    print("Inspection scheduled: PASS")
