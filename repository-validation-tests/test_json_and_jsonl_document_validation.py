# 这是一个 sample，文件实质完成后删掉这行注释

import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "validate_json_and_jsonl_documents.py"


def test_all_json_and_jsonl_documents_parse_successfully():
    result = subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=REPOSITORY_ROOT, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
