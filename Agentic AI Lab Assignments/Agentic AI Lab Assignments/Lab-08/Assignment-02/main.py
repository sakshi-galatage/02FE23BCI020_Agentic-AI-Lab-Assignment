
from concurrent.futures import ThreadPoolExecutor


def research_agent(goal):
    return {
        "role": "research",
        "output": "Plan a 24-hour AI hackathon."
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
        "output": "Innovation, technical depth and demo quality."
    }


ROLES = {
    "research": research_agent,
    "logistics": logistics_agent,
    "budget": budget_agent,
    "judging": judging_agent
}


def run_swarm(goal):
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            name: pool.submit(agent, goal)
            for name, agent in ROLES.items()
        }

        return {
            name: future.result()
            for name, future in futures.items()
        }


def merge(outputs):
    return {
        "format": outputs["research"]["output"],
        "venue": outputs["logistics"]["output"]["venue"],
        "venue_cost": outputs["logistics"]["output"]["venue_cost"],
        "date": outputs["logistics"]["output"]["date"],
        "budget_cap": outputs["budget"]["output"]["total_cap"],
        "judging": outputs["judging"]["output"]
    }


# Each role independently checks the merged plan
def research_critique(plan):
    objections = []
    if not plan["format"]:
        objections.append("Research: Hackathon format is missing.")
    return objections


def logistics_critique(plan):
    objections = []
    if plan["venue_cost"] > plan["budget_cap"]:
        objections.append("Logistics: Venue cost exceeds the available budget.")
    return objections


def budget_critique(plan):
    objections = []
    if plan["venue_cost"] > plan["budget_cap"]:
        objections.append("Budget: Total venue cost is above the budget cap.")
    return objections


def judging_critique(plan):
    objections = []
    if not plan["judging"]:
        objections.append("Judging: Judging criteria are missing.")
    return objections


CRITICS = {
    "research": research_critique,
    "logistics": logistics_critique,
    "budget": budget_critique,
    "judging": judging_critique
}


def distributed_critique(plan):
    conflict_log = []

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            role: pool.submit(critic, plan)
            for role, critic in CRITICS.items()
        }

        for role, future in futures.items():
            objections = future.result()

            for objection in objections:
                conflict_log.append({
                    "raised_by": role,
                    "objection": objection
                })

    return conflict_log


if __name__ == "__main__":
    print("=== Parallel Agent Outputs ===")
    outputs = run_swarm("Plan a college AI hackathon")

    for role, result in outputs.items():
        print(role, ":", result["output"])

    print("\n=== Merged Plan ===")
    plan = merge(outputs)
    print(plan)

    print("\n=== Distributed Critique ===")
    conflict_log = distributed_critique(plan)

    for conflict in conflict_log:
        print(conflict)

    print("\n=== Final Conflict Log ===")
    print(conflict_log)
