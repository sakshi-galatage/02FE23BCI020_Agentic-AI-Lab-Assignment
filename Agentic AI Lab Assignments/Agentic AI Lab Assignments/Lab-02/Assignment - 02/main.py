
import csv
import io
import json

CSV_DATA = """event,signups,category
AI Club Talk,12,technical
Hackathon Kickoff,9,technical
Robotics Demo,15,technical
Cultural Fest,20,social
Music Night,18,social
GenAI Workshop,7,technical
"""

def read_csv():
    reader = csv.DictReader(io.StringIO(CSV_DATA))
    rows = list(reader)
    return {
        "rows": rows,
        "row_count": len(rows)
    }


def filter_by_category(rows, category):
    filtered = [
        row for row in rows
        if row["category"].lower() == category.lower()
    ]

    return {
        "filtered_rows": filtered,
        "count": len(filtered)
    }


def calculator(operation, values):
    if not values:
        return {"error": "No values provided"}

    if operation == "average":
        return {"result": sum(values) / len(values)}

    return {"error": "Unsupported operation"}


TOOLS = {
    "read_csv": read_csv,
    "filter_by_category": filter_by_category,
    "calculator": calculator
}


class CampusDataAssistant:

    def __init__(self):
        self.trace = []

    def call_tool(self, tool_name, reason, **kwargs):

        result = TOOLS[tool_name](**kwargs)

        self.trace.append({
            "tool": tool_name,
            "reason": reason,
            "input": kwargs,
            "output": result
        })

        return result

    def answer(self, question):

        if "technical" in question.lower():

            # Tool 1: Read CSV
            csv_result = self.call_tool(
                "read_csv",
                "Read event sign-up data from the CSV file."
            )

            # Tool 2: Filter technical events
            filter_result = self.call_tool(
                "filter_by_category",
                "Select only technical events as requested.",
                rows=csv_result["rows"],
                category="technical"
            )

            # Validate filter output before calculation
            filtered_rows = filter_result["filtered_rows"]

            if not filtered_rows:
                return "No technical events found. Average cannot be calculated."

            print("\nFiltered technical events:")
            print(json.dumps(filtered_rows, indent=4))

            # Extract sign-up numbers
            values = [
                int(row["signups"])
                for row in filtered_rows
            ]

            # Tool 3: Calculate average
            average_result = self.call_tool(
                "calculator",
                "Calculate average sign-ups of the filtered technical events.",
                operation="average",
                values=values
            )

            return (
                "Average sign-ups for technical events: "
                + str(round(average_result["result"], 2))
            )

        return "Question not supported."


if __name__ == "__main__":

    assistant = CampusDataAssistant()

    question = "What's the average sign-up for technical events only?"

    print("QUESTION:", question)

    answer = assistant.answer(question)

    print("\nFINAL ANSWER:")
    print(answer)

    print("\n=== THREE-TOOL EXECUTION TRACE ===")

    for index, entry in enumerate(assistant.trace, 1):
        print(f"\nSTEP {index}")
        print("Tool:", entry["tool"])
        print("Reason:", entry["reason"])
        print("Input:", entry["input"])
        print("Output:", entry["output"])
