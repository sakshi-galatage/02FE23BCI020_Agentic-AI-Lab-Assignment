
from datetime import datetime


# ---- Tools ----
def tool_word_count(text):
    return {"count": len(text.split())}


def tool_lookup_contact(name, contacts_db):
    return contacts_db.get(name, {"error": f"no contact found for {name}"})


TOOLS = {
    "word_count": tool_word_count,
    "lookup_contact": tool_lookup_contact
}


# ---- Memory ----
class Memory:
    def __init__(self):
        self._store = {}

    def scope(self, user):
        return self._store.setdefault(user, {})


# ---- Audit ----
class Audit:
    def __init__(self):
        self.entries = []

    def log(self, task, skill_name, tool_calls, result=None, error=None):
        self.entries.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "task": task,
            "skill": skill_name,
            "tool_calls": tool_calls,
            "result": result,
            "error": error
        })


# ---- Skills ----
class SummarizeNotesSkill:
    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        text = task.get("text", "")
        wc = TOOLS["word_count"](text)
        self.tool_calls.append({"tool": "word_count", "output": wc})
        self.memory_scope["last_note_length"] = wc["count"]
        return f"Summary stub: note has {wc['count']} words."


class DraftEmailSkill:
    CONTACTS = {
        "Dr. Meena": {"email": "meena@example.edu"}
    }

    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        contact = TOOLS["lookup_contact"](task["to"], self.CONTACTS)
        self.tool_calls.append({
            "tool": "lookup_contact",
            "output": contact
        })

        if "error" in contact:
            raise RuntimeError(contact["error"])

        return f"Draft email to {contact['email']}: '{task['subject']}'"


class TranslateTextSkill:
    def __init__(self, memory_scope):
        self.memory_scope = memory_scope
        self.tool_calls = []

    def execute(self, task):
        return f"[translated to {task['target_lang']}] {task['text']}"


SKILL_REGISTRY = {
    "summarize_notes": SummarizeNotesSkill,
    "draft_email": DraftEmailSkill
}


# ---- Runtime core loop ----
def select_skill(task):
    return task["skill"]


def run_task(task, user, memory, audit):
    skill_name = select_skill(task)
    skill_cls = SKILL_REGISTRY[skill_name]
    skill = skill_cls(memory.scope(user))

    try:
        result = skill.execute(task)
        audit.log(task, skill_name, skill.tool_calls, result=result)
        return result

    except Exception as e:
        audit.log(task, skill_name, skill.tool_calls, error=str(e))
        raise


# ---- Interface with failure escalation ----
def receive_task(task, user, memory, audit):
    skill_name = task["skill"]

    # Count previous failures for this user and skill
    failure_count = sum(
        1 for entry in audit.entries
        if entry["task"].get("user") == user
        and entry["skill"] == skill_name
        and entry["error"] is not None
    )

    task_record = dict(task)
    task_record["user"] = user

    # Escalate after two previous failures
    if failure_count >= 2:
        message = (
            f"Escalated to human: User '{user}' "
            f"has failed skill '{skill_name}' twice."
        )

        audit.log(
            task_record,
            skill_name,
            [],
            error=message
        )

        return message

    return run_task(task_record, user, memory, audit)


# ---- Main Program ----
if __name__ == "__main__":
    memory = Memory()
    audit = Audit()

    user = "user1"

    print("=== Attempt 1: First Failure ===")
    try:
        receive_task(
            {"skill": "draft_email", "to": "Unknown Person", "subject": "Hello"},
            user, memory, audit
        )
    except RuntimeError as e:
        print(f"Task failed: {e}")

    print("\n=== Attempt 2: Second Failure ===")
    try:
        receive_task(
            {"skill": "draft_email", "to": "Unknown Person", "subject": "Hello"},
            user, memory, audit
        )
    except RuntimeError as e:
        print(f"Task failed: {e}")

    print("\n=== Attempt 3: Should Escalate to Human ===")
    result = receive_task(
        {"skill": "draft_email", "to": "Unknown Person", "subject": "Hello"},
        user, memory, audit
    )
    print(result)

    print("\n=== Audit Log ===")
    for entry in audit.entries:
        print(entry)
