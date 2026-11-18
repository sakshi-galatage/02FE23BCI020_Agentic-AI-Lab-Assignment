
"""
Lab 12 - Assignment 01
A Cost-Category Control

Reject proposals when:
1. Cost estimate is missing.
2. Cost exceeds budget without finance approval.
"""

class ProdChangeAgent:
    def __init__(self, budget_threshold):
        self.budget_threshold = budget_threshold
        self.audit_log = []

    def propose_change(self, action, cost_estimate=None, finance_approved=False):
        if cost_estimate is None:
            result = {
                "rejected": True,
                "reason": "Cost estimate is missing."
            }

        elif cost_estimate < 0:
            result = {
                "rejected": True,
                "reason": "Invalid cost estimate."
            }

        elif cost_estimate > self.budget_threshold and not finance_approved:
            result = {
                "rejected": True,
                "reason": "Cost exceeds budget. Finance approval required."
            }

        else:
            result = {
                "rejected": False,
                "action": action,
                "estimated_cost": cost_estimate,
                "reason": "Proposal accepted for human approval."
            }

        self.audit_log.append({
            "action": action,
            "cost_estimate": cost_estimate,
            "finance_approved": finance_approved,
            "result": result
        })

        return result


if __name__ == "__main__":
    agent = ProdChangeAgent(budget_threshold=5000)

    print("=== Budget Threshold ===")
    print("Maximum allowed budget: Rs. 5000")

    print("\n=== Test 1: Cost Within Budget ===")
    print(agent.propose_change(
        action="Restart application server",
        cost_estimate=3000
    ))

    print("\n=== Test 2: Cost Exceeds Budget Without Approval ===")
    print(agent.propose_change(
        action="Replace production database",
        cost_estimate=8000
    ))

    print("\n=== Test 3: Cost Exceeds Budget With Finance Approval ===")
    print(agent.propose_change(
        action="Upgrade production database",
        cost_estimate=8000,
        finance_approved=True
    ))

    print("\n=== Test 4: Adversarial Test - Missing Cost Estimate ===")
    print(agent.propose_change(
        action="Attempt to bypass budget control"
    ))

    print("\n=== Final Audit Log ===")
    for entry in agent.audit_log:
        print(entry)
