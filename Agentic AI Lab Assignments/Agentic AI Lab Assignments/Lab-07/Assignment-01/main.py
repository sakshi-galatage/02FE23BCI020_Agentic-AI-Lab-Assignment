
"""
Lab 7: Agentic Node Graph - Campus Event App
Assignment 1: Add a Security-Scan Node
"""

class Node:
    def __init__(self, name, owner, success_fn, on_success, on_fail):
        self.name = name
        self.owner = owner
        self.success_fn = success_fn
        self.on_success = on_success
        self.on_fail = on_fail


# ---- Node Functions ----

def requirement_node(state):
    state["requirements"] = [
        "user login",
        "event listing",
        "RSVP button"
    ]
    return state


def planner_node(state):
    state["tasks"] = {
        req: f"task_for({req})"
        for req in state["requirements"]
    }
    return state


def builder_node(state):
    if state.get("force_build_fail"):
        state["build_ok"] = False
        return state

    state["build_ok"] = True
    state["code"] = "app.py generated"
    return state


# New security scan node
def security_scan_node(state):
    print("Security scan: Checking generated application...")

    if state.get("force_security_fail"):
        state["security_ok"] = False
        state["security_issues"] = ["SQL injection vulnerability detected"]
    else:
        state["security_ok"] = True
        state["security_issues"] = []

    return state


def tester_node(state):
    state["tests_passed"] = (
        state.get("build_ok", False)
        and state.get("security_ok", False)
    )
    return state


def reviewer_node(state):
    state["review_clean"] = state.get("tests_passed", False)
    return state


def human_gate_node(state):
    state["human_signoff"] = state.get("review_clean", False)
    return state


# ---- Graph Definition ----

GRAPH = [
    Node(
        "requirement",
        "requirement_agent",
        lambda s: len(s.get("requirements", [])) >= 3,
        requirement_node,
        "escalate_to_human"
    ),

    Node(
        "planner",
        "planner_agent",
        lambda s: all(
            r in s.get("tasks", {})
            for r in s.get("requirements", [])
        ),
        planner_node,
        "return_to_requirement"
    ),

    Node(
        "builder",
        "builder_agent",
        lambda s: s.get("build_ok", False),
        builder_node,
        "retry_build_or_escalate"
    ),

    # New node inserted between builder and tester
    Node(
        "security_scan",
        "security_agent",
        lambda s: s.get("security_ok", False),
        security_scan_node,
        "fix_security_issues_or_escalate"
    ),

    Node(
        "tester",
        "tester_agent",
        lambda s: s.get("tests_passed", False),
        tester_node,
        "route_back_to_builder"
    ),

    Node(
        "reviewer",
        "reviewer_agent",
        lambda s: s.get("review_clean", False),
        reviewer_node,
        "route_back_to_builder"
    ),

    Node(
        "human_gate",
        "human",
        lambda s: s.get("human_signoff", False),
        human_gate_node,
        "return_to_planner"
    )
]


# ---- Simulation ----

def simulate(force_build_fail=False, force_security_fail=False):
    state = {
        "force_build_fail": force_build_fail,
        "force_security_fail": force_security_fail
    }

    trace = []

    for node in GRAPH:
        state = node.on_success(state)
        ok = node.success_fn(state)

        trace.append({
            "node": node.name,
            "owner": node.owner,
            "success": ok,
            "state_after": {
                k: v for k, v in state.items()
                if not k.startswith("force_")
            }
        })

        if not ok:
            trace.append({
                "node": node.name,
                "failure_behavior_triggered": node.on_fail
            })
            break

    return trace


# ---- Main Program ----

if __name__ == "__main__":

    print("=== SUCCESS PATH ===")
    for step in simulate():
        print(step)

    print("\n=== FAILURE PATH: SECURITY SCAN FAILS ===")
    for step in simulate(force_security_fail=True):
        print(step)
