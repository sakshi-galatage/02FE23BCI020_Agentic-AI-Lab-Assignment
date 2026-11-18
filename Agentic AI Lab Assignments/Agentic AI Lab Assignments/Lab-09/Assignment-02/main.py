
"""
Lab 9: Deep Research Agent
Assignment 2: Weight Sources by Quality
"""

SOURCES = [
    {
        "id": "S1",
        "type": "peer-reviewed paper",
        "quality_tier": "peer-reviewed",
        "claim": "RAG reduces hallucination rate by 41% on domain QA.",
        "evidence": "200 held-out questions from a medical knowledge base.",
        "limitation": "Small, single-domain evaluation set."
    },
    {
        "id": "S2",
        "type": "vendor engineering blog",
        "quality_tier": "vendor blog",
        "claim": "RAG improves answer accuracy by 35% in support-ticket QA.",
        "evidence": "Internal A/B test over 10,000 tickets.",
        "limitation": "No independent replication reported."
    },
    {
        "id": "S3",
        "type": "independent benchmark report",
        "quality_tier": "independent benchmark",
        "claim": "RAG introduces a latency overhead of 200-400ms per query.",
        "evidence": "Benchmarked across 5 open-source RAG pipelines.",
        "limitation": "Not tested at large scale."
    },
    {
        "id": "S4",
        "type": "independent research study",
        "quality_tier": "independent benchmark",
        "claim": "RAG showed no measurable reduction in hallucination rate.",
        "evidence": "Evaluation on a different domain and a larger test dataset.",
        "limitation": "Results may differ with other datasets and evaluation methods."
    }
]


def build_evidence_table(sources):
    return sources


def compare(sources):
    return {
        "conflicts": [
            {
                "source_1": "S1",
                "source_2": "S4",
                "description": (
                    "S1 reports a 41% reduction in hallucinations, "
                    "while S4 reports no measurable reduction."
                )
            }
        ]
    }


def synthesize(evidence_table, comparison):
    lines = []

    for source in evidence_table:
        lines.append(
            f"[{source['id']}] "
            f"({source['quality_tier']}) {source['claim']}"
        )

    for conflict in comparison["conflicts"]:
        s1 = next(
            s for s in evidence_table
            if s["id"] == conflict["source_1"]
        )
        s4 = next(
            s for s in evidence_table
            if s["id"] == conflict["source_2"]
        )

        quality_order = {
            "peer-reviewed": 3,
            "independent benchmark": 2,
            "vendor blog": 1
        }

        if quality_order[s1["quality_tier"]] > quality_order[s4["quality_tier"]]:
            preferred = s1
            down_weighted = s4
        else:
            preferred = s4
            down_weighted = s1

        lines.append(
            f"\n[Conflict: {s1['id']} vs {s4['id']}] "
            f"{conflict['description']}"
        )

        lines.append(
            f"Synthesis leans toward {preferred['id']} because "
            f"its source quality tier is higher "
            f"({preferred['quality_tier']})."
        )

        lines.append(
            f"{down_weighted['id']} is down-weighted because its quality "
            f"tier is lower ({down_weighted['quality_tier']}), "
            f"but its claim is not discarded."
        )

    return lines


if __name__ == "__main__":
    table = build_evidence_table(SOURCES)

    print("=== Evidence Table with Quality Tiers ===")
    for row in table:
        print(row)

    comparison = compare(table)

    print("\n=== Source Comparison ===")
    print(comparison)

    synthesis = synthesize(table, comparison)

    print("\n=== Quality-Weighted Executive Summary ===")
    for line in synthesis:
        print(line)
