import threading
import time
from datetime import datetime, timezone

class DemoBot:
    """
    Safe demo worker. It does not connect to Free Fire, send invitations,
    generate authentication tokens, or interact with third-party accounts.
    Replace only with an authorized, documented integration.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._thread = None
        self._stop_event = threading.Event()
        self._running = False
        self._started_at = None
        self._label = "Idle"
        self._cycles = 0
        self._logs = []

    def _log(self, message):
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        with self._lock:
            self._logs.insert(0, f"{stamp} — {message}")
            self._logs = self._logs[:30]

    def start(self, label="Demo run"):
        with self._lock:
            if self._running:
                return
            self._stop_event.clear()
            self._running = True
            self._started_at = datetime.now(timezone.utc).isoformat()
            self._label = label
            self._cycles = 0
        self._log(f"Demo worker started: {label}")
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while not self._stop_event.wait(3):
            with self._lock:
                self._cycles += 1
                cycle = self._cycles
            self._log(f"Demo heartbeat #{cycle} — no game/network actions performed")
        with self._lock:
            self._running = False
        self._log("Demo worker stopped")

    def stop(self):
        self._stop_event.set()
        self._log("Stop requested")

    def status(self):
        with self._lock:
            return {
                "running": self._running,
                "label": self._label,
                "started_at": self._started_at,
                "cycles": self._cycles,
                "logs": list(self._logs),
                "mode": "SAFE DEMO — no external game connection"
            }

bot = DemoBot()
