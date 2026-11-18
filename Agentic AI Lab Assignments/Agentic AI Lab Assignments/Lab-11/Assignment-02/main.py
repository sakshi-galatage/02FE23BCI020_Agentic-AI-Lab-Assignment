
"""
Lab 11 - Assignment 02
Prove test independence with a deliberate bug.
The coding agent has an inverted filter condition.
The testing agent remains unchanged and tests the acceptance criteria.
"""

FEATURE_REQUEST = "Export the filtered report as CSV."


def requirement_agent(request):
    return {
        "id": "US-1",
        "acceptance_criteria": [
            "CSV output is generated",
            "Only rows matching the applied filters are exported",
            "CSV header matches visible columns"
        ]
    }


def coding_agent(story):
    # DELIBERATE BUG:
    # Should be row.get(k) == v
    # Incorrectly uses !=, exporting the wrong rows.
    def export_endpoint(rows, applied_filters, columns):
        filtered = [
            row for row in rows
            if all(row.get(k) != v for k, v in applied_filters.items())
        ]

        lines = [",".join(columns)]
        for row in filtered:
            lines.append(",".join(str(row.get(c, "")) for c in columns))

        return "\n".join(lines)

    return export_endpoint


def testing_agent(story):
    # Tests are generated only from acceptance criteria.
    # This function is NOT changed to match the buggy code.
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
            ("header matches columns",
             output.splitlines()[0] == "region,sales"),
            ("only filtered rows present",
             all("South" not in line for line in output.splitlines()[1:]))
        ]

        return results, acceptance_criteria

    return test_suite


if __name__ == "__main__":
    story = requirement_agent(FEATURE_REQUEST)

    print("=== User Story ===")
    print(story)

    export_fn = coding_agent(story)
    test_suite = testing_agent(story)

    results, criteria = test_suite(export_fn)

    print("\n=== Independent Test Results ===")
    print("Acceptance criteria:", criteria)

    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}")

    print("\n=== Bug Evidence ===")
    print("Expected: Only North rows should be exported.")
    print("Actual CSV output:")
    print(export_fn(
        [
            {"region": "North", "sales": 100},
            {"region": "South", "sales": 200},
            {"region": "North", "sales": 150}
        ],
        {"region": "North"},
        ["region", "sales"]
    ))

    print("\n=== Lineage ===")
    print("Story <- requirement_agent(request)")
    print("Code <- coding_agent(story) [contains deliberate bug]")
    print("Tests <- testing_agent(story) [independent of code]")
