
class Node:
    def __init__(self, name, owner, success_fn, action, on_fail):
        self.name = name
        self.owner = owner
        self.success_fn = success_fn
        self.action = action
        self.on_fail = on_fail


def requirement_node(state):
    state["requirements"] = ["user login", "event listing", "RSVP button"]
    return state


def planner_node(state):
    state["tasks"] = {
        req: f"task_for({req})"
        for req in state["requirements"]
    }
    return state


def builder_node(state):
    state["build_attempts"] += 1

    if state["build_attempts"] <= state["fail_attempts"]:
        state["build_ok"] = False
        print("Builder failed on attempt", state["build_attempts"])
    else:
        state["build_ok"] = True
        state["code"] = "app.py generated"
        print("Builder succeeded on attempt", state["build_attempts"])

    return state


def tester_node(state):
    state["tests_passed"] = state.get("build_ok", False)
    return state


def reviewer_node(state):
    state["review_clean"] = state.get("tests_passed", False)
    return state


def human_gate_node(state):
    state["human_signoff"] = state.get("review_clean", False)
    return state


GRAPH = [
    Node(
        "requirement", "requirement_agent",
        lambda s: len(s.get("requirements", [])) >= 3,
        requirement_node,
        "escalate_to_human"
    ),
    Node(
        "planner", "planner_agent",
        lambda s: all(req in s.get("tasks", {}) for req in s.get("requirements", [])),
        planner_node,
        "return_to_requirement"
    ),
    Node(
        "builder", "builder_agent",
        lambda s: s.get("build_ok", False),
        builder_node,
        "retry_once_or_escalate"
    ),
    Node(
        "tester", "tester_agent",
        lambda s: s.get("tests_passed", False),
        tester_node,
        "return_to_builder"
    ),
    Node(
        "reviewer", "reviewer_agent",
        lambda s: s.get("review_clean", False),
        reviewer_node,
        "return_to_builder"
    ),
    Node(
        "human_gate", "human",
        lambda s: s.get("human_signoff", False),
        human_gate_node,
        "return_to_planner"
    )
]


def simulate(fail_attempts):
    state = {
        "build_attempts": 0,
        "fail_attempts": fail_attempts
    }

    trace = []

    for node in GRAPH:
        if node.name == "builder":
            while state["build_attempts"] < 2:
                state = node.action(state)

                if node.success_fn(state):
                    break

                if state["build_attempts"] == 1:
                    print("Retrying builder once...")
                else:
                    print("Retry limit reached. Escalating to human.")
                    trace.append({
                        "node": node.name,
                        "owner": node.owner,
                        "success": False,
                        "failure_behavior_triggered": "escalate_to_human"
                    })
                    return trace

        else:
            state = node.action(state)

        ok = node.success_fn(state)

        trace.append({
            "node": node.name,
            "owner": node.owner,
            "success": ok,
            "state_after": {
                key: value for key, value in state.items()
                if key != "fail_attempts"
            }
        })

        if not ok:
            trace.append({
                "node": node.name,
                "failure_behavior_triggered": node.on_fail
            })
            break

    return trace


print("=== CASE 1: BUILDER FAILS ONCE AND SUCCEEDS ON RETRY ===")
for item in simulate(fail_attempts=1):
    print(item)

print("\n=== CASE 2: BUILDER FAILS TWICE AND ESCALATES ===")
for item in simulate(fail_attempts=2):
    print(item)
