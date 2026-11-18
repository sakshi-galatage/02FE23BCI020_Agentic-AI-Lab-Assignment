
"""
Lab 9: Deep Research Agent
Assignment 1: Add a Directly Contradicting Source
"""

QUESTION = (
    "What are the demonstrated benefits and limitations of "
    "retrieval-augmented generation (RAG) for domain-specific question answering?"
)

SOURCES = [
    {
        "id": "S1",
        "type": "peer-reviewed paper",
        "date": "2026-02",
        "claim": "RAG reduces hallucination rate by 41% on domain QA.",
        "evidence": "200 held-out questions from a medical knowledge base.",
        "limitation": "Small, single-domain evaluation set."
    },
    {
        "id": "S2",
        "type": "vendor engineering blog",
        "date": "2026-04",
        "claim": "RAG improves answer accuracy by 35% in support-ticket QA.",
        "evidence": "Internal A/B test over 10,000 tickets.",
        "limitation": "No independent replication reported."
    },
    {
        "id": "S3",
        "type": "independent benchmark report",
        "date": "2026-05",
        "claim": "RAG introduces a latency overhead of 200-400ms per query.",
        "evidence": "Benchmarked across 5 open-source RAG pipelines.",
        "limitation": "Not tested at large scale."
    },
    {
        "id": "S4",
        "type": "independent research study",
        "date": "2026-06",
        "claim": "RAG showed no measurable reduction in hallucination rate.",
        "evidence": "Evaluation on a different domain and a larger test dataset.",
        "limitation": "Results may differ with other datasets and evaluation methods."
    }
]


def build_evidence_table(sources):
    return sources


def compare(sources):
    agreements = []
    conflicts = []
    gaps = []

    s1 = next(s for s in sources if s["id"] == "S1")
    s4 = next(s for s in sources if s["id"] == "S4")

    if "reduces hallucination" in s1["claim"] and "no measurable reduction" in s4["claim"]:
        conflicts.append(
            "S1 reports a 41% reduction in hallucinations, "
            "while S4 reports no measurable reduction. "
            "This is a direct contradiction. "
            "A possible reason is different evaluation methodology, "
            "domain, and dataset size."
        )

    agreements.append(
        "S1 and S2 both report improvements in RAG answer quality."
    )

    gaps.append(
        "No source in this set reports on RAG performance for non-English languages."
    )

    return {
        "agreements": agreements,
        "conflicts": conflicts,
        "gaps": gaps
    }


def synthesize(evidence_table, comparison):
    lines = []

    for source in evidence_table:
        lines.append(f"[{source['id']}] {source['claim']}")

    for agreement in comparison["agreements"]:
        lines.append(f"[S1,S2] Agreement: {agreement}")

    for conflict in comparison["conflicts"]:
        lines.append(f"[S1,S4] DIRECT CONFLICT: {conflict}")

    for gap in comparison["gaps"]:
        lines.append(f"[gap] {gap}")

    return lines


if __name__ == "__main__":
    print("=== Research Question ===")
    print(QUESTION)

    table = build_evidence_table(SOURCES)

    print("\n=== Evidence Table ===")
    for row in table:
        print(row)

    comparison = compare(table)

    print("\n=== Comparison ===")
    print(comparison)

    synthesis = synthesize(table, comparison)

    print("\n=== Executive Summary ===")
    for line in synthesis:
        print(line)

    print("\n=== Recommended Next Questions ===")
    print("- Why do S1 and S4 report different hallucination results?")
    print("- How does dataset size affect RAG evaluation?")
