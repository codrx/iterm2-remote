
from iterm2 import Session, Connection
import iterm2


#TODO

def get_current_terminal() -> Session:
    async def get(connection: Connection):
        app = await iterm2.async_get_app(connection)
        session = app.current_terminal_window.current_tab.current_session
        return session

    iterm2.run_until_complete(get)


