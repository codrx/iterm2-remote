
import daemon
import signal

from server import serve

def shutdown(signum, frame):
    raise SystemExit(0)

with daemon.DaemonContext(
    signal_map = { 
        signal.SIGTERM: shutdown,
        signal.SIGINT: shutdown 
    }
):
    serve()