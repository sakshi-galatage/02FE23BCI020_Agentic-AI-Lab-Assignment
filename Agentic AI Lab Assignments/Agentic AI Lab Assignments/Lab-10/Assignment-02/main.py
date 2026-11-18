
"""
Lab 10: Cloud Operations Agent
Assignment 2: A Safe Auto-Remediation Path
"""

def classify_severity(error_rate):
    if error_rate >= 50:
        return "ALARM"
    elif error_rate >= 2:
        return "WARNING"
    return "NORMAL"


def propose_action(severity):
    if severity == "WARNING":
        return {
            "action": "restart_single_pod",
            "risk_level": "low"
        }

    if severity == "ALARM":
        return {
            "action": "rollback_deployment",
            "risk_level": "high"
        }

    return {
        "action": "no_action",
        "risk_level": "low"
    }


def execute_or_request_approval(proposal):
    action = proposal["action"]
    risk = proposal["risk_level"]

    print(f"Proposed action: {action}")
    print(f"Risk level: {risk}")

    # Rollback-class actions always require approval.
    if "rollback" in action:
        print("Result: Approval requested from human.")
        print("Action NOT auto-executed.")
        return "approval_required"

    # Only low-risk actions can execute automatically.
    if risk == "low":
        print("Result: Action automatically executed.")
        return "auto_executed"

    print("Result: Human approval required.")
    return "approval_required"


if __name__ == "__main__":

    print("=== Scenario 1: WARNING Incident ===")
    warning_severity = classify_severity(5)
    print("Severity:", warning_severity)

    warning_proposal = propose_action(warning_severity)
    warning_result = execute_or_request_approval(warning_proposal)

    print("\n=== Scenario 2: ALARM Incident ===")
    alarm_severity = classify_severity(60)
    print("Severity:", alarm_severity)

    alarm_proposal = propose_action(alarm_severity)
    alarm_result = execute_or_request_approval(alarm_proposal)

    print("\n=== Safety Verification ===")
    assert warning_result == "auto_executed"
    assert alarm_result == "approval_required"

    print("WARNING action executed automatically: PASS")
    print("Rollback action requires approval: PASS")
    print("Rollback was never auto-executed: PASS")
