
"""
Lab 6: OpenCLA/OpenClaw Runtime
Assignment 1: Add Per-User Rate Limiting
Maximum 3 tasks per user per session.
"""

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


# ---- Memory, scoped per user ----

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
        self.tool_calls.append({"tool": "lookup_contact", "output": contact})

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


# ---- Runtime core loop (unchanged) ----

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


# ---- Interface with rate limiting ----

def receive_task(task, user, memory, audit):
    user_task_count = sum(
        1 for entry in audit.entries
        if entry["task"].get("user") == user
    )

    if user_task_count >= 3:
        return f"Task rejected: User '{user}' has reached the 3-task limit."

    task["user"] = user
    return run_task(task, user, memory, audit)


# ---- Main program ----

if __name__ == "__main__":
    memory = Memory()
    audit = Audit()

    SKILL_REGISTRY["translate_text"] = TranslateTextSkill

    print("=== Task 1 ===")
    print(receive_task(
        {"skill": "summarize_notes", "text": "Agentic AI systems combine goals tools skills memory"},
        "user1", memory, audit
    ))

    print("\n=== Task 2 ===")
    print(receive_task(
        {"skill": "draft_email", "to": "Dr. Meena", "subject": "Lab guide review"},
        "user1", memory, audit
    ))

    print("\n=== Task 3 ===")
    print(receive_task(
        {"skill": "translate_text", "text": "Hello team", "target_lang": "Kannada"},
        "user1", memory, audit
    ))

    print("\n=== Task 4: Should Be Rejected ===")
    print(receive_task(
        {"skill": "summarize_notes", "text": "This is the fourth task"},
        "user1", memory, audit
    ))

    print("\n=== Audit Log ===")
    for entry in audit.entries:
        print(entry)
