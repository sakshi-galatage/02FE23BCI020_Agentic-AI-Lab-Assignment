
"""
Lab 10: Cloud Operations Agent
Assignment 1: A Second Incident Type
"""

# Scenario 1: Payments service incident
PAYMENTS_LOGS = [
    {"ts": "14:00:00", "level": "INFO", "msg": "payments-service v2.4.1 deploy started"},
    {"ts": "14:00:45", "level": "INFO", "msg": "payments-service deploy completed"},
    {"ts": "14:03:10", "level": "WARN", "msg": "refund endpoint latency elevated"},
    {"ts": "14:03:40", "level": "ERROR", "msg": "refund endpoint NullPointerException"},
    {"ts": "14:04:05", "level": "ERROR", "msg": "refund endpoint NullPointerException"},
]

PAYMENTS_DEPLOYS = [
    {
        "ts": "14:00:00",
        "service": "payments-service",
        "version": "v2.4.1",
        "prev_version": "v2.4.0"
    }
]

PAYMENTS_METRICS = {
    "baseline_error_rate": 0.5,
    "current_error_rate": 1.6
}


# Scenario 2: Database connection-pool exhaustion
DATABASE_LOGS = [
    {"ts": "15:00:00", "level": "INFO", "msg": "database-service v1.8.0 deploy started"},
    {"ts": "15:00:30", "level": "INFO", "msg": "database-service deploy completed"},
    {"ts": "15:02:10", "level": "WARN", "msg": "database connection pool usage at 85%"},
    {"ts": "15:03:00", "level": "ERROR", "msg": "database connection pool exhausted"},
    {"ts": "15:03:30", "level": "ERROR", "msg": "database connection timeout"},
]

DATABASE_DEPLOYS = [
    {
        "ts": "15:00:00",
        "service": "database-service",
        "version": "v1.8.0",
        "prev_version": "v1.7.5"
    }
]

DATABASE_METRICS = {
    "baseline_error_rate": 0.5,
    "current_error_rate": 60.0
}


def classify_severity(metrics):
    ratio = metrics["current_error_rate"] / metrics["baseline_error_rate"]

    if metrics["current_error_rate"] > 50:
        return "down"
    if ratio >= 2:
        return "degraded"
    return "early_warning"


def find_incident_start(logs):
    for entry in logs:
        if entry["level"] == "ERROR":
            return entry["ts"]
    return None


def correlate_with_recent_changes(logs, deploys, incident_start):
    error_messages = [
        entry["msg"].lower()
        for entry in logs
        if entry["level"] == "ERROR"
    ]

    if any("connection pool" in msg or "connection timeout" in msg
           for msg in error_messages):
        affected_path = "database connection pool"
    elif any("refund" in msg for msg in error_messages):
        affected_path = "refund endpoint"
    else:
        affected_path = "unknown"

    for deploy in deploys:
        if (incident_start and deploy["ts"] < incident_start
                and deploy["service"].lower().startswith(
                    ("payments", "database")
                )):
            return {
                "hypothesis": (
                    f"Errors started at {incident_start}, shortly after "
                    f"the deployment of {deploy['service']} "
                    f"{deploy['version']}. Errors are concentrated in "
                    f"the {affected_path} path, suggesting a possible "
                    f"regression in that release."
                ),
                "suspect_deploy": deploy,
                "affected_path": affected_path
            }

    return {
        "hypothesis": "No recent deployment correlates with the incident.",
        "suspect_deploy": None,
        "affected_path": affected_path
    }


def diagnose(logs, deploys, metrics):
    severity = classify_severity(metrics)
    incident_start = find_incident_start(logs)
    hypothesis = correlate_with_recent_changes(
        logs, deploys, incident_start
    )

    return {
        "severity": severity,
        "incident_start": incident_start,
        "diagnosis": hypothesis["hypothesis"],
        "affected_path": hypothesis["affected_path"],
        "suspect_deploy": hypothesis["suspect_deploy"]
    }


if __name__ == "__main__":
    print("=== Scenario 1: Payments Service ===")
    payments_result = diagnose(
        PAYMENTS_LOGS, PAYMENTS_DEPLOYS, PAYMENTS_METRICS
    )
    for key, value in payments_result.items():
        print(f"{key}: {value}")

    print("\n=== Scenario 2: Database Pool Exhaustion ===")
    database_result = diagnose(
        DATABASE_LOGS, DATABASE_DEPLOYS, DATABASE_METRICS
    )
    for key, value in database_result.items():
        print(f"{key}: {value}")

    print("\n=== Comparison ===")
    print("Payments severity:", payments_result["severity"])
    print("Database severity:", database_result["severity"])
    print("Payments affected path:", payments_result["affected_path"])
    print("Database affected path:", database_result["affected_path"])

    assert payments_result["severity"] != database_result["severity"], (
        "The two scenarios should produce different severity levels."
    )

    assert payments_result["affected_path"] != database_result["affected_path"]

    print("\nConfirmed: Both incidents have different diagnoses and severity.")
