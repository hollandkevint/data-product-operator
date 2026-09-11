"""Check evidence-graph structure without executing skills or fetching evidence."""
import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = Path(__file__).resolve().parents[1] / "example.json"
FIELDS = {"question": ["owner"], "definition": ["version"],
          "source": ["version", "locator"], "check": ["method", "expected", "state", "basis"],
          "finding": ["basis"], "decision": ["state", "owner", "scope", "review_trigger"],
          "outcome": ["state", "window"]}
STATES = {"check": {"proposed", "executed"}, "decision": {"pending", "hold", "accepted"},
          "outcome": {"pending", "observed"}}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(graph):
    require(isinstance(graph, dict), "Expected graph object")
    require(isinstance(graph.get("revision"), str) and graph["revision"].strip(), "Missing revision")
    require(isinstance(graph.get("nodes"), list) and graph["nodes"], "Missing nodes")
    nodes = {}
    for n in graph["nodes"]:
        require(isinstance(n, dict), "Expected node object")
        for field in ["id", "kind", "summary"]:
            require(isinstance(n.get(field), str) and n[field].strip(), f"Missing {field}")
        key, kind = n["id"], n["kind"]
        require(key not in nodes and kind in FIELDS, f"{key}: Duplicate ID or unknown kind")
        for field in FIELDS[kind]:
            require(isinstance(n.get(field), str) and n[field].strip(), f"{key}: Missing {field}")
        for field in ["depends_on", "skills"]:
            require(isinstance(n.get(field), list) and all(isinstance(x, str) and x.strip() for x in n[field]), f"{key}: Invalid {field}")
            require(len(n[field]) == len(set(n[field])), f"{key}: Duplicate {field}")
        for skill in n["skills"]:
            path = (ROOT / skill).resolve()
            require(path.is_relative_to(ROOT / "skills") and path.name == "SKILL.md" and path.is_file(), f"{key}: Missing or unsafe skill path")
        if kind in STATES:
            require(n["state"] in STATES[kind], f"{key}: Invalid state")
        require(isinstance(n.get("stale", False), bool), f"{key}: stale must be boolean")
        if kind == "check":
            require(n["basis"] in {"observed", "synthetic"}, f"{key}: Invalid basis")
            if n["state"] == "executed":
                require(all(isinstance(n.get(f), str) and n[f].strip() for f in ["result", "run_ref"]), f"{key}: Execution needs result and run_ref")
            else:
                require(n.get("result") is None and n.get("run_ref") is None, f"{key}: Proposed check claims execution")
        if kind == "finding":
            require(n["basis"] in {"observation", "interpretation", "hypothesis"}, f"{key}: Invalid basis")
        if kind == "outcome" and n["state"] == "observed":
            require(isinstance(n.get("evidence"), str) and n["evidence"].strip(), f"{key}: Missing outcome evidence")
        nodes[key] = n
    ancestors = {}
    def visit(key, active):
        require(key in nodes, f"Missing dependency: {key}")
        require(key not in active, f"Dependency cycle: {key}")
        if key not in ancestors:
            parents = set(nodes[key]["depends_on"])
            result = set(parents)
            for parent in parents:
                result.update(visit(parent, active | {key}))
            ancestors[key] = result
        return ancestors[key]
    needs = {"definition": {"question"}, "check": {"definition", "source"},
             "finding": {"check"}, "decision": {"finding"}, "outcome": {"decision"}}
    for key, n in nodes.items():
        upstream = [nodes[p] for p in visit(key, set())]
        require(needs.get(n["kind"], set()) <= {p["kind"] for p in upstream}, f"{key}: Incomplete evidence path")
        if n["kind"] == "finding" and n["basis"] == "observation":
            require(all(p["state"] == "executed" for p in upstream if p["kind"] == "check"), f"{key}: Observation needs executed checks")
        if n["kind"] == "decision" and n["state"] == "accepted":
            require(not any(p.get("stale", False) for p in upstream + [n]), f"{key}: Stale evidence")
            checks = [p for p in upstream if p["kind"] == "check"]
            require(checks and all(p["state"] == "executed" and p["basis"] == "observed" for p in checks), f"{key}: Acceptance needs observed executed checks")
            require(not any(p["kind"] == "finding" and p["basis"] == "hypothesis" for p in upstream), f"{key}: Unresolved hypothesis")
    return nodes


def affected(nodes, changed):
    require(changed in nodes, f"Unknown changed ID: {changed}")
    seen = {changed}
    while True:
        following = {key for key, n in nodes.items() if seen.intersection(n["depends_on"])} - seen
        if not following:
            return sorted(seen - {changed})
        seen.update(following)


def self_test():
    graph = json.loads(EXAMPLE.read_text())
    assert affected(validate(graph), "s1") == ["c1", "f1", "j1", "o1"]
    cases = [(0, {"id": "s1"}), (3, {"depends_on": ["d1", "missing"]}),
             (0, {"depends_on": ["o1"]}), (2, {"version": ""}),
             (3, {"state": "executed"}), (3, {"result": "Invented pass"}),
             (5, {"state": "accepted"}), (6, {"state": "observed"}),
             (3, {"depends_on": ["s1"]}), (3, {"skills": ["../../outside/SKILL.md"]}),
             (3, {"basis": "certified"}), (4, {"basis": "observation"})]
    for index, update in cases:
        bad = copy.deepcopy(graph)
        bad["nodes"][index].update(update)
        try:
            validate(bad)
        except ValueError:
            continue
        raise AssertionError(f"Invalid graph accepted: {update}")
    control = copy.deepcopy(graph)
    control["nodes"][3].update(state="executed", basis="observed", result="Structural test only", run_ref="fictional-self-test")
    control["nodes"][4]["basis"] = "observation"
    control["nodes"][5]["state"] = "accepted"
    validate(control)  # Well-formed evidence can still be false; this tool cannot verify it.
    control["nodes"][2]["stale"] = True
    try:
        validate(control)
    except ValueError:
        pass
    else:
        raise AssertionError("Stale evidence accepted")
    print("PASS: Example, downstream traversal, 13 rejection cases and structural acceptance control")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", nargs="?", type=Path, default=EXAMPLE)
    parser.add_argument("--affected", metavar="ID")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
        else:
            nodes = validate(json.loads(args.graph.read_text()))
            print(json.dumps({"structure": "valid", "nodes": len(nodes), "requires_review": affected(nodes, args.affected) if args.affected else [], "limit": "No evidence contents or release authority verified"}))
    except (ValueError, OSError, RecursionError) as error:
        parser.exit(1, f"Invalid graph: {error}\n")
