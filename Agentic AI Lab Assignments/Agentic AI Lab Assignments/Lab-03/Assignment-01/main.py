
# Lab 03 - Assignment 01
# Handle a Multi-Claim Source

ARTICLE_C = {
    "title": "AI System Performance and Cost Study",
    "text": """
    The new AI system reduced operating costs by 20%.
    The study tested this claim on only 5 small projects.

    The AI system improved prediction accuracy by 35%.
    This result was measured using 500 test samples across 10 projects.
    """
}


def apply_research_summary_skill(article):
    text = article["text"]

    cost_claim = {
        "claim": "The AI system reduced operating costs by 20%.",
        "evidence": "The claim was tested on only 5 small projects.",
        "strength": 1
    }

    accuracy_claim = {
        "claim": "The AI system improved prediction accuracy by 35%.",
        "evidence": "The result was measured using 500 test samples across 10 projects.",
        "strength": 2
    }

    # Compare the supporting evidence
    claims = [cost_claim, accuracy_claim]
    selected_claim = max(claims, key=lambda x: x["strength"])

    result = {
        "claim": selected_claim["claim"],
        "evidence": selected_claim["evidence"],
        "selection_note": (
            "Two competing claims were identified: cost reduction "
            "and accuracy improvement. The accuracy claim was selected "
            "because it has stronger supporting evidence."
        ),
        "limitation": (
            "The study provides limited information about whether "
            "the results generalize to other systems and settings."
        ),
        "takeaway": (
            "When comparing research claims, prefer the claim "
            "supported by stronger and more extensive evidence."
        )
    }

    return result


def main():
    result = apply_research_summary_skill(ARTICLE_C)

    print("=== RESEARCH SUMMARY SKILL ===")
    print("Article:", ARTICLE_C["title"])

    print("\nSelected Claim:")
    print(result["claim"])

    print("\nSupporting Evidence:")
    print(result["evidence"])

    print("\nSelection Explanation:")
    print(result["selection_note"])

    print("\nLimitation:")
    print(result["limitation"])

    print("\nTeaching Takeaway:")
    print(result["takeaway"])


if __name__ == "__main__":
    main()
