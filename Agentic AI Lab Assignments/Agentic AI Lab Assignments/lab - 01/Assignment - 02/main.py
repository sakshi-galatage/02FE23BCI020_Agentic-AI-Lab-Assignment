
import json

SIMULATED_ANSWERS = {
    "subjects": ["Data Structures", "Operating Systems", "AI Agents"],
    "hours_per_day": 2,
    "unavailable_days": ["Sunday"]
}


class StudyPlannerAgent:

    def __init__(self):
        self.goal = {
            "subjects": None,
            "hours_per_day": None,
            "unavailable_days": None,
            "schedule_generated": False
        }

        self.plan = None
        self.log = []

    def read_existing_schedule(self):
        # Two days are already busy
        return {
            "busy_days": ["Wednesday", "Friday"]
        }

    def _build_plan(self, schedule):

        busy_days = schedule["busy_days"]
        unavailable_days = self.goal["unavailable_days"]

        # Find busy days not mentioned by the student
        conflicts = [
            day for day in busy_days
            if day not in unavailable_days
        ]

        if conflicts:
            print("\n!!! SCHEDULING CONFLICT DETECTED !!!")
            print("Your selected unavailable days:", unavailable_days)
            print("Existing busy days:", busy_days)
            print("Conflict found on:", conflicts)
            print("These busy days will be excluded from your study plan.\n")

            self.log.append({
                "action": "Scheduling conflict detected",
                "conflicting_days": conflicts,
                "message": "Busy days were not included in unavailable days."
            })

        # Exclude both unavailable and busy days
        all_days = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ]

        available_days = [
            day for day in all_days
            if day not in unavailable_days
            and day not in busy_days
        ]

        subjects = self.goal["subjects"]
        plan = {}

        for i, day in enumerate(available_days):
            plan[day] = {
                "subject": subjects[i % len(subjects)],
                "time": "17:00-19:00"
            }

        return plan

    def run(self):

        # Collect student requirements
        for field in ["subjects", "hours_per_day", "unavailable_days"]:
            self.goal[field] = SIMULATED_ANSWERS[field]

            self.log.append({
                "action": "Collected " + field,
                "observed": self.goal[field]
            })

        # Read existing schedule
        schedule = self.read_existing_schedule()

        print("Existing schedule:", schedule)

        self.log.append({
            "action": "Read existing schedule",
            "observed": schedule
        })

        # Detect conflicts and build a safe plan
        self.plan = self._build_plan(schedule)

        self.goal["schedule_generated"] = True

        self.log.append({
            "action": "Generated conflict-free study plan",
            "observed": self.plan
        })

        return self.plan


if __name__ == "__main__":

    agent = StudyPlannerAgent()

    print("=== STUDY PLANNER AGENT ===")

    plan = agent.run()

    print("=== FINAL STUDY PLAN ===")
    print(json.dumps(plan, indent=4))

    print("\n=== FULL AGENT LOG ===")

    for entry in agent.log:
        print(json.dumps(entry, indent=4))

    print("\nAgent completed successfully.")
