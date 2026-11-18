
from dataclasses import dataclass
from datetime import date


@dataclass
class MemoryRecord:
    topic: str
    fact: str
    saved_date: date


class ProjectMemory:
    def __init__(self, retention_days=30):
        self.records = {}
        self.retention_days = retention_days

    def save(self, topic, fact, saved_date):
        self.records[topic] = MemoryRecord(
            topic, fact, saved_date
        )
        print(f"Memory saved: {topic} = {fact}")

    def retrieve(self, topic):
        return self.records.get(topic)


class ProjectAssistant:
    def __init__(self, memory):
        self.memory = memory

    def answer(self, topic, today):
        record = self.memory.retrieve(topic)

        if record is None:
            return "Information not available."

        age = (today - record.saved_date).days

        if age > self.memory.retention_days:
            print(
                f"WARNING: This decision is from {age} days ago "
                "and may be out of date."
            )

        return (
            f"Answer: {record.fact} "
            f"(Saved on {record.saved_date})"
        )


# Main program
memory = ProjectMemory(retention_days=30)
assistant = ProjectAssistant(memory)

today = date(2026, 11, 17)

print("=== PROJECT MEMORY RETENTION TEST ===")
print("Retention period:", memory.retention_days, "days")

# Fresh record: 10 days old
memory.save(
    "frontend",
    "React",
    date(2026, 11, 7)
)

# Old record: 60 days old
memory.save(
    "database",
    "PostgreSQL",
    date(2026, 9, 18)
)

print("\n=== FRESH MEMORY TEST ===")
print(assistant.answer("frontend", today))

print("\n=== OLD MEMORY TEST ===")
print(assistant.answer("database", today))

print("\n=== UNKNOWN MEMORY TEST ===")
print(assistant.answer("cloud", today))
