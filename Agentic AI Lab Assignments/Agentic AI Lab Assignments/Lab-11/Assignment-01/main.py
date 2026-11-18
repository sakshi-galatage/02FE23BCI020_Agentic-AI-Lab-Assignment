
"""
Lab 11: Agentic SDLC Factory
Assignment 1: A Second, Concurrent Story
"""

FEATURE_REQUESTS = [
    "Add CSV export to the reports page, preserving applied filters.",
    "Add PDF export to the reports page, preserving applied filters."
]


def requirement_agent(requests):
    stories = []

    for i, request in enumerate(requests, start=1):
        if "CSV" in request:
            story = {
                "id": "US-1",
                "format": "CSV",
                "text": "As a user, I can export the filtered report as a CSV file.",
                "acceptance_criteria": [
                    "CSV file is generated",
                    "Only filtered rows are exported",
                    "CSV header matches visible columns"
                ]
            }
        else:
            story = {
                "id": "US-2",
                "format": "PDF",
                "text": "As a user, I can export the filtered report as a PDF file.",
                "acceptance_criteria": [
                    "PDF file is generated",
                    "Only filtered rows are exported",
                    "PDF contains visible column names"
                ]
            }

        stories.append(story)

    return stories


def design_agent(story):
    return {
        "story_id": story["id"],
        "format": story["format"],
        "components": [
            f"{story['format'].lower()}_export_endpoint",
            f"{story['format'].lower()}_serializer",
            "export_button"
        ]
    }


def coding_agent(design, story):
    export_format = story["format"]

    def export_endpoint(rows, applied_filters, columns):
        filtered = [
            row for row in rows
            if all(row.get(key) == value
                   for key, value in applied_filters.items())
        ]

        if export_format == "CSV":
            output = [",".join(columns)]
            for row in filtered:
                output.append(
                    ",".join(str(row.get(column, "")) for column in columns)
                )
            return "\n".join(output)

        else:
            output = ["PDF REPORT"]
            output.append(" | ".join(columns))
            for row in filtered:
                output.append(
                    " | ".join(str(row.get(column, "")) for column in columns)
                )
            return "\n".join(output)

    return {
        "story_id": story["id"],
        "format": export_format,
        "export_endpoint": export_endpoint
    }


def testing_agent(story):
    """Tests are created from acceptance criteria, not implementation."""

    acceptance_criteria = story["acceptance_criteria"]

    def test_suite(export_fn):
        rows = [
            {"region": "North", "sales": 100},
            {"region": "South", "sales": 200},
            {"region": "North", "sales": 150}
        ]

        columns = ["region", "sales"]
        output = export_fn(rows, {"region": "North"}, columns)

        results = [
            ("produces output", len(output) > 0),
            ("contains correct column names",
             all(column in output for column in columns)),
            ("only filtered rows present", "South" not in output)
        ]

        return results, acceptance_criteria

    return test_suite


def review_agent(design, code, test_results):
    issues = []

    if design["story_id"] != code["story_id"]:
        issues.append("Design and code story IDs do not match.")

    if not all(passed for _, passed in test_results):
        issues.append("One or more tests failed.")

    return {
        "story_id": code["story_id"],
        "issues": issues,
        "clean": len(issues) == 0
    }


def run_pipeline(story):
    print(f"\n========== {story['id']} : {story['format']} EXPORT ==========")

    design = design_agent(story)
    print("Design:", design)

    code = coding_agent(design, story)

    # Testing agent receives only the story.
    test_suite = testing_agent(story)
    test_results, criteria = test_suite(code["export_endpoint"])

    print("Acceptance criteria:", criteria)

    for name, passed in test_results:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")

    review = review_agent(design, code, test_results)
    print("Review:", review)

    print("Lineage:")
    print(f"Story: {story['id']}")
    print(f"Design: {design['story_id']}")
    print(f"Code: {code['story_id']}")
    print(f"Tests: testing_agent({story['id']}) [independent of code]")
    print(f"Review: {review['story_id']}")

    return {
        "story_id": story["id"],
        "design": design,
        "code": code,
        "review": review
    }


if __name__ == "__main__":
    stories = requirement_agent(FEATURE_REQUESTS)

    print("=== Generated User Stories ===")
    for story in stories:
        print(story)

    print("\n=== Human Checkpoint ===")
    print("Both feature requirements confirmed.")

    results = []

    for story in stories:
        results.append(run_pipeline(story))

    print("\n=== Final Pipeline Summary ===")
    for result in results:
        print(
            result["story_id"],
            result["code"]["format"],
            "Accepted" if result["review"]["clean"] else "Rejected"
        )

    print("\n=== Final Lineage Trace ===")
    print("US-1 -> CSV Design -> CSV Code -> CSV Tests -> CSV Review")
    print("US-2 -> PDF Design -> PDF Code -> PDF Tests -> PDF Review")
