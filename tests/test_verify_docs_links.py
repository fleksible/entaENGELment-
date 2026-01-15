import subprocess
import sys


def test_verify_docs_links():
    result = subprocess.run(
        [sys.executable, "-m", "tools.verify_docs_links"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
