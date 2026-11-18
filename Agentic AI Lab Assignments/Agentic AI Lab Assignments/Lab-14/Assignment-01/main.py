
from datetime import datetime

# ---------------- TOOLS ----------------

FAQ_DB = {
    "wifi": "Connect to Campus-Secure using your student ID."
}

TICKET_DB = []


def tool_search_faq(query):
    for key, answer in FAQ_DB.items():
        if key in query.lower():
            return {"found": True, "answer": answer}
    return {"found": False}


def tool_create_ticket(issue):
    ticket_id = f"T-{len(TICKET_DB) + 1:03d}"
    TICKET_DB.append({
        "id": ticket_id,
        "issue": issue,
        "status": "open"
    })
    return {"ticket_id": ticket_id}


def tool_check_ticket_status(ticket_id):
    for ticket in TICKET_DB:
        if ticket["id"] == ticket_id:
            return ticket
    return {"error": "Ticket not found"}


# ---------------- SKILL 1 ----------------

def triage_skill(issue_text):
    """Search FAQ first. Never invent an FAQ answer."""

    faq = tool_search_faq(issue_text)

    if faq["found"]:
        return {
            "skill": "triage_skill",
            "resolution": "faq",
            "answer": faq["answer"]
        }

    ticket = tool_create_ticket(issue_text)

    return {
        "skill": "triage_skill",
        "resolution": "escalated",
        "ticket_id": ticket["ticket_id"]
    }


# ---------------- SKILL 2 ----------------

def password_reset_skill(issue_text):
    """Give safe password-reset guidance.
    Never ask users to share their password or OTP.
    """

    return {
        "skill": "password_reset_skill",
        "resolution": "guidance",
        "instructions": [
            "Open the official college password reset page.",
            "Enter your registered student email.",
            "Verify your identity using the official process.",
            "Create a new strong password.",
            "Never share your password or OTP with anyone."
        ]
    }


# ---------------- MEMORY ----------------

class CapstoneMemory:

    def __init__(self):
        self.session = {}
        self.history = []

    def record(self, user, issue, outcome):
        entry = {
            "user": user,
            "issue": issue,
            "outcome": outcome,
            "date": datetime.now().isoformat(timespec="seconds")
        }

        self.history.append(entry)
        self.session["last_issue"] = issue


# ---------------- NODE GRAPH ----------------

def node_graph_run(user, issue, memory, audit_log, prompt_log):

    prompt_log.append({
        "stage": "intake",
        "input": issue
    })

    # Safety control
    if not issue.strip():
        audit_log.append({
            "stage": "intake",
            "result": "rejected: empty issue"
        })

        return {
            "rejected": True,
            "reason": "Empty issue text"
        }

    # Route to the correct reusable skill
    if "password" in issue.lower() or "reset" in issue.lower():
        outcome = password_reset_skill(issue)
    else:
        outcome = triage_skill(issue)

    prompt_log.append({
        "stage": "skill_execution",
        "output": outcome
    })

    if outcome["resolution"] == "faq":
        response = outcome["answer"]

    elif outcome["resolution"] == "guidance":
        response = "\n".join(outcome["instructions"])

    else:
        response = (
            f"Support ticket {outcome['ticket_id']} created."
        )

    memory.record(user, issue, outcome)

    audit_log.append({
        "stage": "complete",
        "user": user,
        "issue": issue,
        "skill": outcome["skill"],
        "outcome": outcome
    })

    return {
        "rejected": False,
        "response": response,
        "outcome": outcome
    }


# ---------------- MAIN PROGRAM ----------------

if __name__ == "__main__":

    memory = CapstoneMemory()
    audit_log = []
    prompt_log = []

    print("=== RUN 1: WIFI ISSUE ===")

    r1 = node_graph_run(
        "alice",
        "How do I connect to wifi?",
        memory,
        audit_log,
        prompt_log
    )

    print(r1)

    print("\n=== RUN 2: PASSWORD RESET ===")

    r2 = node_graph_run(
        "bob",
        "I need help with password reset",
        memory,
        audit_log,
        prompt_log
    )

    print(r2)

    print("\n=== RUN 3: UNKNOWN ISSUE ===")

    r3 = node_graph_run(
        "carol",
        "My laptop charger is broken",
        memory,
        audit_log,
        prompt_log
    )

    print(r3)

    print("\n=== RUN 4: EMPTY INPUT SAFETY CHECK ===")

    r4 = node_graph_run(
        "david",
        " ",
        memory,
        audit_log,
        prompt_log
    )

    print(r4)

    print("\n=== SKILL VERIFICATION ===")

    assert r1["outcome"]["skill"] == "triage_skill"
    assert r2["outcome"]["skill"] == "password_reset_skill"
    assert r3["outcome"]["resolution"] == "escalated"
    assert r4["rejected"] is True

    print("Triage skill: PASS")
    print("Password reset skill: PASS")
    print("Unknown issue escalation: PASS")
    print("Empty input safety control: PASS")

    print("\n=== PROMPT LOG ===")
    for item in prompt_log:
        print(item)

    print("\n=== AUDIT LOG ===")
    for item in audit_log:
        print(item)

    print("\n=== MEMORY HISTORY ===")
    for item in memory.history:
        print(item)
