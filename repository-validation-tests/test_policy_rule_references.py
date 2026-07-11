# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "validate_repository_cross_references.py"


def load_script_module():
    spec = spec_from_file_location("cross_reference_validator", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_all_policy_rule_references_resolve_in_current_repository():
    module = load_script_module()
    policy_ids = module.load_policy_rule_ids(REPOSITORY_ROOT)
    references = module.find_policy_rule_references(REPOSITORY_ROOT)
    unknown = sorted({policy_id for _, policy_id in references if policy_id not in policy_ids})
    assert unknown == []


def test_unknown_policy_reference_is_detected(tmp_path):
    module = load_script_module()
    policy_register = tmp_path / "shared-writing-harness/harness-policies/policy-rule-register.jsonl"
    policy_register.parent.mkdir(parents=True)
    policy_register.write_text(
        json.dumps(
            {
                "policy_rule_id": "POLICY-FACTUALITY-001",
                "policy_file": "policy.md",
                "rule_summary": "Known rule.",
                "enforcement_scope": ["test"],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (tmp_path / "document.md").write_text(
        "Required policy: `POLICY-UNKNOWN-999`.\n",
        encoding="utf-8",
    )

    policy_ids = module.load_policy_rule_ids(tmp_path, policy_register)
    references = module.find_policy_rule_references(tmp_path)
    unknown = sorted({policy_id for _, policy_id in references if policy_id not in policy_ids})
    assert unknown == ["POLICY-UNKNOWN-999"]
