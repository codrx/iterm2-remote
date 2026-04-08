
from iterm2 import Session, Connection
import asyncio
import iterm2 


def jump_terminal(current_session: Session, other_session: Session):

    async def jump(connection: Connection):
        other_session.async_activate()

    iterm2.run_until_complete(jump)

# peek another terminal from your terminal
def peek_terminal(current_session: Session, other_session: Session, length: int) -> None:

    async def peek(connection: Connection):
        other_session.async_activate()
        asyncio.sleep(length)
        current_session.async_activate()

    iterm2.run_until_complete(peek)


    