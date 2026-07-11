# 这是一个 sample，文件实质完成后删掉这行注释

import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "validate_sample_comment_markers.py"


def test_every_repository_file_contains_the_sample_marker():
    result = subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=REPOSITORY_ROOT, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
