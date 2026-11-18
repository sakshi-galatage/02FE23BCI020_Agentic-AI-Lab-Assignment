
"""
Lab 13 - Assignment 01
Add a Second Domain: Electrical Load Forecasting

Mechanical agent: Predictive maintenance.
Electrical agent: Electricity load forecasting.
Safety: ALARM recommendations always require human review.
"""

# ---------------- MECHANICAL ENGINEERING ----------------

MECHANICAL_LOG = [
    {"t": 0, "vibration": 1.8, "temp": 61},
    {"t": 1, "vibration": 2.4, "temp": 65},
    {"t": 2, "vibration": 3.1, "temp": 70},
    {"t": 3, "vibration": 4.6, "temp": 76},
    {"t": 4, "vibration": 6.2, "temp": 84}
]

MECHANICAL_THRESHOLDS = {
    "vibration_warn": 2.8,
    "vibration_alarm": 4.5,
    "temp_warn": 70,
    "temp_alarm": 80
}


def mechanical_agent():
    latest = MECHANICAL_LOG[-1]

    if (latest["vibration"] >= MECHANICAL_THRESHOLDS["vibration_alarm"]
            or latest["temp"] >= MECHANICAL_THRESHOLDS["temp_alarm"]):
        condition = "ALARM"
        action = "Recommend shutdown for human review"

    elif (latest["vibration"] >= MECHANICAL_THRESHOLDS["vibration_warn"]
            or latest["temp"] >= MECHANICAL_THRESHOLDS["temp_warn"]):
        condition = "WARNING"
        action = "Schedule maintenance inspection"

    else:
        condition = "NORMAL"
        action = "Continue monitoring"

    return {
        "domain": "Mechanical Engineering",
        "latest_reading": latest,
        "condition": condition,
        "recommended_action": action,
        "auto_executed": condition == "NORMAL"
    }


# ---------------- ELECTRICAL ENGINEERING ----------------

ELECTRICAL_LOG = [
    {"hour": 1, "load_kw": 40},
    {"hour": 2, "load_kw": 45},
    {"hour": 3, "load_kw": 55},
    {"hour": 4, "load_kw": 68},
    {"hour": 5, "load_kw": 92}
]

LOAD_THRESHOLDS = {
    "warning": 60,
    "alarm": 85
}


def electrical_agent():
    latest = ELECTRICAL_LOG[-1]
    load = latest["load_kw"]

    if load >= LOAD_THRESHOLDS["alarm"]:
        condition = "ALARM"
        action = "Recommend load reduction for human review"

    elif load >= LOAD_THRESHOLDS["warning"]:
        condition = "WARNING"
        action = "Schedule electrical load inspection"

    else:
        condition = "NORMAL"
        action = "Continue normal load monitoring"

    return {
        "domain": "Electrical Engineering - Load Forecasting",
        "latest_reading": latest,
        "condition": condition,
        "recommended_action": action,
        "auto_executed": condition == "NORMAL"
    }


# ---------------- MAIN PROGRAM ----------------

if __name__ == "__main__":

    print("=== MECHANICAL ENGINEERING AGENT ===")
    mechanical_result = mechanical_agent()

    for key, value in mechanical_result.items():
        print(f"{key}: {value}")

    print("\n=== ELECTRICAL ENGINEERING AGENT ===")
    electrical_result = electrical_agent()

    for key, value in electrical_result.items():
        print(f"{key}: {value}")

    print("\n=== SAFETY VERIFICATION ===")

    for result in [mechanical_result, electrical_result]:
        if result["condition"] == "ALARM":
            assert result["auto_executed"] is False
            print(
                f"{result['domain']}: ALARM requires human review - PASS"
            )

    print("\nConfirmed: Neither agent automatically executes ALARM actions.")
