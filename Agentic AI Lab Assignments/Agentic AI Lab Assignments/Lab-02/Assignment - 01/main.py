
import csv
import io
import json

SIGNUPS_CSV = """event,signups
AI Club Talk,12
Hackathon Kickoff,9
Robotics Demo,15
GenAI Workshop,7
Capstone Expo,20
Career Panel,11
"""

MOCK_EVENTS_API_DB = {
    "AI Club Talk": {
        "date": "2026-07-02",
        "location": "CS Block Auditorium"
    },
    "Hackathon Kickoff": {
        "date": "2026-07-05",
        "location": "Innovation Lab"
    }
}

THRESHOLD = 13


def calculator(operation, values):
    if operation == "average":
        if not values:
            return {"error": "no values supplied"}
        return {"result": sum(values) / len(values)}

    if operation == "sum":
        return {"result": sum(values)}

    return {"error": f"unsupported operation: {operation}"}


def read_csv(source_text=SIGNUPS_CSV):
    reader = csv.DictReader(io.StringIO(source_text))
    rows = list(reader)

    if not rows:
        return {
            "error": "empty file",
            "rows": [],
            "row_count": 0
        }

    return {
        "rows": rows,
        "row_count": len(rows)
    }


def mock_events_api(event_name):
    record = MOCK_EVENTS_API_DB.get(event_name)

    if record is None:
        return {
            "error": f"no event metadata found for '{event_name}'"
        }

    return record


# This tool only drafts a notification.
# It does not send any message.
def send_notification(message):
    return {
        "status": "Draft created",
        "message": message,
        "sent": False
    }


TOOLS = {
    "calculator": calculator,
    "read_csv": read_csv,
    "events_api": mock_events_api,
    "send_notification": send_notification
}


class CampusDataAssistant:

    def __init__(self):
        self.trace = []

    def _call(self, tool_name, reason, **kwargs):

        result = TOOLS[tool_name](**kwargs)

        entry = {
            "tool": tool_name,
            "reason": reason,
            "input": kwargs,
            "output": result
        }

        self.trace.append(entry)

        if "error" in result:
            raise RuntimeError(
                f"{tool_name} failed: {result['error']}"
            )

        return result

    def answer(self, question):

        q = question.lower()

        if "average" in q and "sign" in q:

            csv_result = self._call(
                "read_csv",
                "Sign-up counts are stored in the CSV file."
            )

            values = [
                int(row["signups"])
                for row in csv_result["rows"]
            ]

            total = self._call(
                "calculator",
                "Calculate the total number of sign-ups.",
                operation="sum",
                values=values
            )

            avg = self._call(
                "calculator",
                "Calculate the average sign-ups per event.",
                operation="average",
                values=values
            )

            average_value = avg["result"]

            answer = (
                f"Total sign-ups: {total['result']}. "
                f"Average per event: {average_value:.2f} "
                f"(across {csv_result['row_count']} events)."
            )

            # Draft a notification if average is below threshold
            if average_value < THRESHOLD:

                message = (
                    f"Low turnout notice: Average event sign-ups "
                    f"are {average_value:.2f}, which is below "
                    f"the threshold of {THRESHOLD}. "
                    f"Please promote upcoming campus events."
                )

                notification = self._call(
                    "send_notification",
                    "Average sign-ups are below the threshold, "
                    "so a low-turnout notice must be drafted.",
                    message=message
                )

                answer += (
                    "\nNotification: "
                    + notification["status"]
                    + ". It has NOT been sent."
                )

            return answer

        if "where" in q and "hackathon" in q:

            meta = self._call(
                "events_api",
                "Event date and location are stored in the events API.",
                event_name="Hackathon Kickoff"
            )

            return (
                f"Hackathon Kickoff is at {meta['location']} "
                f"on {meta['date']}."
            )

        if "where" in q and "capstone" in q:

            try:
                meta = self._call(
                    "events_api",
                    "Checking the API for Capstone Expo details.",
                    event_name="Capstone Expo"
                )

                return (
                    f"Capstone Expo is at {meta['location']} "
                    f"on {meta['date']}."
                )

            except RuntimeError:
                return (
                    "I don't have location/date metadata "
                    "for Capstone Expo in the events API."
                )

        return "I don't have a tool path configured for that question."


if __name__ == "__main__":

    assistant = CampusDataAssistant()

    questions = [
        "How many students signed up for events this month, and what's the average per event?",
        "Where and when is the Hackathon Kickoff?",
        "Where and when is the Capstone Expo?"
    ]

    for question in questions:
        print("\nQ:", question)
        print("A:", assistant.answer(question))

    print("\n=== FULL TOOL TRACE ===")

    for i, entry in enumerate(assistant.trace, 1):
        print(f"\n{i}. Tool: {entry['tool']}")
        print("Reason:", entry["reason"])
        print("Input:", entry["input"])
        print("Output:", entry["output"])
