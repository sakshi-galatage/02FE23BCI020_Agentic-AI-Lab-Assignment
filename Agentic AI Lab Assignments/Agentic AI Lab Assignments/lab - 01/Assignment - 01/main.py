
import json
import copy

SIMULATED_ANSWERS = {
    "subjects": ["Data Structures", "Operating Systems", "AI Agents"],
    "hours_per_day": 2,
    "unavailable_days": ["Sunday"]
}

FEEDBACK_ROUND_1 = "Move Tuesday's session to the evening."
FEEDBACK_ROUND_2 = "Make Friday's session shorter, only one hour."


class StudyPlannerAgent:
    def __init__(self, existing_schedule):
        self.goal = {
            "subjects": None,
            "hours_per_day": None,
            "unavailable_days": None,
            "schedule_generated": False
        }
        self.existing_schedule = existing_schedule
        self.plan = None
        self.log = []

    def satisfied(self):
        return self.goal["schedule_generated"] is True

    def next_step(self):
        for field in ["subjects", "hours_per_day", "unavailable_days"]:
            if self.goal[field] is None:
                return "ask", field
        return "generate_plan", None

    def read_existing_schedule(self):
        return self.existing_schedule

    def run(self):
        while not self.satisfied():
            step, argument = self.next_step()

            if step == "ask":
                answer = SIMULATED_ANSWERS[argument]
                self.goal[argument] = answer

                self.log.append({
                    "iteration": len(self.log) + 1,
                    "action": f"Asked user for {argument}",
                    "observed": answer,
                    "stopped": False
                })

            elif step == "generate_plan":
                busy = self.read_existing_schedule()

                self.log.append({
                    "iteration": len(self.log) + 1,
                    "action": "Read existing schedule",
                    "observed": busy,
                    "stopped": False
                })

                self.plan = self._build_plan(busy)
                self.goal["schedule_generated"] = True

                self.log.append({
                    "iteration": len(self.log) + 1,
                    "action": "Generated weekly study plan",
                    "observed": copy.deepcopy(self.plan),
                    "stopped": True,
                    "reason": "Study plan generated successfully"
                })

        return self.plan

    def _build_plan(self, busy_slots):
        days = [
            day for day in
            ["Monday", "Tuesday", "Wednesday", "Thursday",
             "Friday", "Saturday", "Sunday"]
            if day not in self.goal["unavailable_days"]
        ]

        subjects = self.goal["subjects"]
        plan = {}

        for i, day in enumerate(days):
            time = "17:00-19:00"

            if day in busy_slots.get("busy_days", []):
                time = "20:00-22:00"

            plan[day] = {
                "subject": subjects[i % len(subjects)],
                "time": time
            }

        return plan

    def revise(self, feedback):
        self.log.append({
            "iteration": len(self.log) + 1,
            "action": "Received feedback: " + feedback,
            "stopped": False
        })

        if "tuesday" in feedback.lower() and "evening" in feedback.lower():
            self.plan["Tuesday"]["time"] = "20:00-22:00"

        if "friday" in feedback.lower() and "one hour" in feedback.lower():
            self.plan["Friday"]["time"] = "17:00-18:00"

        self.log.append({
            "iteration": len(self.log) + 1,
            "action": "Updated existing plan",
            "observed": copy.deepcopy(self.plan),
            "stopped": True,
            "reason": "Feedback applied without regenerating the plan"
        })

        return self.plan


if __name__ == "__main__":
    existing_schedule = {"busy_days": ["Wednesday"]}
    agent = StudyPlannerAgent(existing_schedule)

    print("=== INITIAL STUDY PLAN ===")
    initial_plan = agent.run()
    print(json.dumps(initial_plan, indent=4))

    print("\n=== FIRST FEEDBACK ROUND ===")
    revised_plan_1 = agent.revise(FEEDBACK_ROUND_1)
    print(json.dumps(revised_plan_1, indent=4))

    print("\n=== SECOND FEEDBACK ROUND ===")
    revised_plan_2 = agent.revise(FEEDBACK_ROUND_2)
    print(json.dumps(revised_plan_2, indent=4))

    print("\n=== FULL ITERATION LOG ===")
    for entry in agent.log:
        print(json.dumps(entry, indent=4))

    print("\nBoth feedback rounds completed successfully.")
