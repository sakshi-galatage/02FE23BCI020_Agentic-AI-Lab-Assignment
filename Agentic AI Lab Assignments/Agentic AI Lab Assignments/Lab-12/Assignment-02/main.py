
"""
Lab 12 - Assignment 02
Mandatory Re-Evaluation After Every 5 Proposals

The agent must be re-evaluated after every 5 proposals.
A 6th proposal must be blocked until evaluation() is called again.
"""

class ProdChangeAgent:
    def __init__(self):
        self.proposal_count = 0
        self.evaluated = False
        self.audit_log = []

    def evaluate(self):
        self.evaluated = True
        self.proposal_count = 0

        result = {
            "evaluated": True,
            "message": "Evaluation passed. Agent can propose changes."
        }

        self.audit_log.append({
            "step": "evaluation",
            "result": result
        })

        return result

    def propose_change(self, action):
        if not self.evaluated:
            result = {
                "accepted": False,
                "reason": "Agent must be evaluated before proposing changes."
            }

        elif self.proposal_count >= 5:
            self.evaluated = False
            result = {
                "accepted": False,
                "reason": "5 proposals completed. Re-evaluation required before the next proposal."
            }

        else:
            self.proposal_count += 1
            result = {
                "accepted": True,
                "action": action,
                "proposal_number": self.proposal_count
            }

            if self.proposal_count == 5:
                result["message"] = "Proposal limit reached. Re-evaluation required next."

        self.audit_log.append({
            "step": "proposal",
            "action": action,
            "result": result
        })

        return result


if __name__ == "__main__":
    agent = ProdChangeAgent()

    print("=== Initial Evaluation ===")
    print(agent.evaluate())

    print("\n=== First Five Proposals ===")
    for number in range(1, 6):
        print(f"Proposal {number}:")
        print(agent.propose_change(f"Production change {number}"))

    print("\n=== Sixth Proposal: Must Be Blocked ===")
    print(agent.propose_change("Production change 6"))

    print("\n=== Re-Evaluation ===")
    print(agent.evaluate())

    print("\n=== Sixth Proposal After Re-Evaluation ===")
    print(agent.propose_change("Production change 6"))

    print("\n=== Final Audit Log ===")
    for entry in agent.audit_log:
        print(entry)
