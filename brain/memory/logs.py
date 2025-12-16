from datetime import datetime
from pathlib import Path


class Logger:
    """Simple file-based logging"""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

    def log(self, message: str):
        timestamp = datetime.now().isoformat()
        log_file = self.log_dir / "kernel.log"
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
