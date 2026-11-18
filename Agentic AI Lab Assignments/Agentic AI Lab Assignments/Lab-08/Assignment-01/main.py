
from concurrent.futures import ThreadPoolExecutor


# Four agents with different responsibilities

def research_agent(goal):
    return {
        "role": "research",
        "output": "A 24-hour hackathon with AI and innovation themes."
    }


def logistics_agent(goal):
    return {
        "role": "logistics",
        "output": {
            "venue": "Grand Hall",
            "venue_cost": 45000,
            "date": "Saturday"
        }
    }


def budget_agent(goal):
    return {
        "role": "budget",
        "output": {"total_cap": 30000}
    }


def judging_agent(goal):
    return {
        "role": "judging",
        "output": "Innovation, technical depth, and demo quality."
    }


ROLES = {
    "research": research_agent,
    "logistics": logistics_agent,
    "budget": budget_agent,
    "judging": judging_agent
}


# Run all agents in parallel
def run_swarm(goal):
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            name: pool.submit(agent, goal)
            for name, agent in ROLES.items()
        }

        outputs = {
            name: future.result()
            for name, future in futures.items()
        }

    return outputs


# Merge all agent outputs
def merge(outputs):
    return {
        "format": outputs["research"]["output"],
        "venue": outputs["logistics"]["output"]["venue"],
        "venue_cost": outputs["logistics"]["output"]["venue_cost"],
        "date": outputs["logistics"]["output"]["date"],
        "budget": outputs["budget"]["output"]["total_cap"],
        "judging": outputs["judging"]["output"]
    }


# Identify conflicts between agents
def critique(plan):
    conflicts = []

    if plan["venue_cost"] > plan["budget"]:
        conflicts.append({
            "conflict": "Venue cost exceeds budget",
            "venue_cost": plan["venue_cost"],
            "budget": plan["budget"]
        })

    return conflicts


# Resolve the conflict using a priority rule
def resolve(conflict):
    return {
        "rule": "budget_over_preference",
        "resolution": (
            "Reject the expensive venue and ask logistics "
            "to find an alternative within the budget."
        )
    }


if __name__ == "__main__":
    goal = "Plan a college AI hackathon"

    print("=== Parallel Agent Outputs ===")
    outputs = run_swarm(goal)

    for name, result in outputs.items():
        print(name, ":", result["output"])

    print("\n=== Merged Hackathon Plan ===")
    plan = merge(outputs)
    print(plan)

    print("\n=== Conflict Check ===")
    conflicts = critique(plan)
    print(conflicts)

    print("\n=== Conflict Resolution ===")
    for conflict in conflicts:
        print(resolve(conflict))

    print("\n=== Final Plan ===")
    print("Format:", plan["format"])
    print("Date:", plan["date"])
    print("Venue: Alternative venue within budget")
    print("Budget: Rs.", plan["budget"])
    print("Judging:", plan["judging"])
