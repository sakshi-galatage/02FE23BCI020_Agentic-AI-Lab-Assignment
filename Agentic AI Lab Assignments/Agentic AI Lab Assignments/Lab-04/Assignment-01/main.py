
from dataclasses import dataclass


@dataclass
class MemoryRecord:
    topic: str
    fact: str
    date: str
    source: str


class ProjectMemory:
    def __init__(self):
        self.records = []

    def save(self, topic, fact, date, source, role):
        if role != "team_lead":
            print("Access denied: Only team lead can update memory.")
            return False

        self.records = [
            r for r in self.records if r.topic != topic
        ]

        self.records.append(
            MemoryRecord(topic, fact, date, source)
        )

        print(f"Memory saved: {topic} = {fact}")
        return True

    def retrieve(self, topic):
        for record in self.records:
            if record.topic == topic:
                return record
        return None


class ProjectAssistant:
    def __init__(self, memory):
        self.memory = memory

    def answer(self, topic, session_state=None):
        if session_state and topic in session_state:
            return f"[current session] {session_state[topic]}"

        record = self.memory.retrieve(topic)

        if record:
            return (
                f"[stored memory, dated {record.date}] "
                f"{record.fact}"
            )

        return "[stored memory] Information not available."

    def receive_statement(self, topic, new_fact, role, date):
        old_record = self.memory.retrieve(topic)

        if role != "team_lead":
            if old_record and old_record.fact != new_fact:
                print("\nCONFLICT DETECTED!")
                print("Existing memory:", old_record.fact)
                print("New statement:", new_fact)

            print("Access denied: Only team lead can update memory.")
            return False

        if old_record and old_record.fact != new_fact:
            print("\nCONFLICT DETECTED!")
            print("Existing memory:", old_record.fact)
            print("New statement:", new_fact)
            print("Team lead confirmed the new decision.")

        return self.memory.save(
            topic, new_fact, date, "team decision", role
        )


# Main program
memory = ProjectMemory()
assistant = ProjectAssistant(memory)

print("=== PROJECT MEMORY ASSISTANT ===")

# Store two separate project decisions
assistant.receive_statement(
    "database", "PostgreSQL", "team_lead", "2026-07-03"
)

assistant.receive_statement(
    "hosting", "AWS Cloud", "team_lead", "2026-07-05"
)

# Retrieve each topic independently
print("\n=== DATABASE RETRIEVAL ===")
print("Database:", assistant.answer("database"))

print("\n=== HOSTING RETRIEVAL ===")
print("Hosting:", assistant.answer("hosting"))

# Check that topics do not leak into each other
print("\n=== TOPIC ISOLATION TEST ===")

database_answer = assistant.answer("database")
hosting_answer = assistant.answer("hosting")

print("Database answer contains hosting fact:",
      "AWS Cloud" in database_answer)

print("Hosting answer contains database fact:",
      "PostgreSQL" in hosting_answer)

# Current session information
print("\n=== CURRENT SESSION ===")

session = {
    "database": "Currently reviewing PostgreSQL."
}

print("Database:", assistant.answer("database", session))

# Test conflict detection
print("\n=== CONFLICT CHECK ===")

assistant.receive_statement(
    "database", "SQLite", "team_member", "2026-07-10"
)

# Team lead confirms the change
print("\n=== TEAM LEAD CONFIRMATION ===")

assistant.receive_statement(
    "database", "SQLite", "team_lead", "2026-07-13"
)

# Test unauthorized access
print("\n=== PERMISSION CHECK ===")

assistant.receive_statement(
    "database", "MongoDB", "team_member", "2026-07-14"
)

# Final memory
print("\n=== FINAL PROJECT MEMORY ===")

print("Database:", assistant.answer("database"))
print("Hosting:", assistant.answer("hosting"))
