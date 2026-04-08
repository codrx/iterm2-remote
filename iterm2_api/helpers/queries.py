
from typing import Dict, Optional

from iterm2 import Session, Connection, App
import iterm2


def get_session_by_name(app: App, name: str) -> Optional[Session]:
    for window in app.terminal_windows:
        # I am assuming that there are no terminal windows with multiple tabs for now
        window_session = window.tabs[0].sessions[0]
        print(window_session)
        if window_session.name.split(" ")[0] == name:
            return window_session


def get_all_terminals() -> Dict[int, iterm2.Session]:
    async def get(connection: Connection):
        app = await iterm2.async_get_app(connection)
        return {
            i: window.current_tab.current_session
            for i, window in enumerate(app.terminal_windows)
        }

    return iterm2.run_until_complete(get)
