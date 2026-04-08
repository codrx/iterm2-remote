

"""
    TODO: 

        - need to clean up

        - Fix:

            -> session name changes to ~ when unfocusing terminal

"""   

from typing import Optional

from iterm2 import Session, Connection
import iterm2

from iterm2_api.helpers.queries import get_session_by_name

    
async def send_text_to_session(session: Session, text: str):
    await session.async_send_text(text)


async def send_command_to_session(session: Session, command: str):
    xcommand = command + "\n"
    await session.async_send_text(xcommand)

# ? option in API
async def inject(session: Session, data: bytes):
    pass


def send_to_terminal(
    session_name: Optional[str] = None, 
    session_id: Optional[str] = None,
    command: Optional[str] = None,
    text: Optional[str] = None
) -> bool:

    async def message(connection: Connection):
        try:
            app = await iterm2.async_get_app(connection)

            if app:

                session = None

                # ID doesn't change i believe, while the name does
                if session_id:
                    session = app.get_session_by_id(session_id)
                    print(session)
                else:
                    #TODO: fix
                    if session_name:
                        session = get_session_by_name(app, session_name)

                if session:
                    if command and not text:
                        print(command)
                        await send_command_to_session(session, command)

                    if not command and text:
                        await send_text_to_session(session, text)

                # Doesn't fix issue
                # await self.__session.async_set_name(self.__session_name)

        except Exception as _:
            pass


    if (session_name or session_id) or (command or text):
        iterm2.run_until_complete(message, False)
        return True

    return False


# import argparse

# parser = argparse.ArgumentParser(description="Spawn iterm2 terminal.")

# group1 = parser.add_mutually_exclusive_group(required=True)

# group1.add_argument("--name", 
#                     type=str, 
#                     help="Name of terminal session.", 
#                     required=False)

# group1.add_argument("--id", 
#                     type=str, 
#                     help="Terminal session id.", 
#                     required=False)


# group2 = parser.add_mutually_exclusive_group(required=True)

# group2.add_argument("--command", 
#                     type=str, 
#                     help="Command to send to terminal to be executed, e.g., htop, ls -a.", 
#                     required=False)

# group2.add_argument("--text", 
#                     type=str, 
#                     help="Text to send to terminal.", 
#                     required=False)

# args = parser.parse_args()

# st = SendToTerminal(args.name, args.id, args.command, args.text)
# iterm2.run_until_complete(st.send, False)

# send_to_terminal(args.name, args.id, args.command, args.text)


