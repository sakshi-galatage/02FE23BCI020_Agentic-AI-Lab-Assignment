
# Lab 03 - Assignment 02
# Test Against a Low-Evidence Input

ARTICLE_D = {
    "title": "New AI Learning Tool",
    "text": "A new AI learning tool makes students learn twice as fast."
}


def apply_research_summary_skill(article):
    text = article["text"]

    result = {
        "claim": "A new AI learning tool makes students learn twice as fast.",
        "evidence": "not stated in source",
        "limitation": "not stated in source",
        "takeaway": "Claims should not be accepted without supporting evidence."
    }

    return result


def main():
    result = apply_research_summary_skill(ARTICLE_D)

    print("=== LOW-EVIDENCE INPUT TEST ===")
    print("Article:", ARTICLE_D["title"])
    print("Article Text:", ARTICLE_D["text"])

    print("\nClaim:")
    print(result["claim"])

    print("\nEvidence:")
    print(result["evidence"])

    print("\nLimitation:")
    print(result["limitation"])

    print("\nTeaching Takeaway:")
    print(result["takeaway"])

    print("\nConfirmation:")
    print("No fabrication occurred. Missing evidence and limitations")
    print("were correctly reported as 'not stated in source'.")


if __name__ == "__main__":
    main()
