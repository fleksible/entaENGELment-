import json

def test_policy_loads():
    with open("policies/gate_policy_v1.json") as f:
        p = json.load(f)
    assert "version" in p
