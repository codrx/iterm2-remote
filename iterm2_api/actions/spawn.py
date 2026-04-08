
"""

    - need to separate operations mores??

    TODO: Issues:
        - aliases are not remembered when spawning and directly executing command
        - session names are not changed

    
    TODO: 
        - implement exit delay for commands
            -> currently using unix sleep command can work but not python
            -> from future - idk what this means 

"""


from typing import Optional
# import argparse

from iterm2 import Window, Session, Connection, RPCException
import iterm2


# need class because cannot pass partial function to iterm2.run_until_complete ?
class Terminal:
    def __init__(
        self,
        name: str,
        focus: Optional[bool] = False,
        shell: Optional[str] = None,
        command: Optional[str] = None,
    ):

        self.session = None
        self.window = None
        self.session_id = None
        self.window_id = None

        self.__name = name
        self.__focus = focus
        self.__shell = shell
        self.__command = command


    async def set_window_title(self, window: Window, name: str) -> Optional[RPCException]:
        await window.async_set_title(title=name)


    async def set_session_name(self, session: Session, name: str) -> Optional[RPCException]:
        await session.async_set_name(name=name)


    async def __connect(
        self, shell: Optional[str], command: Optional[str], connection: Connection
    ) -> Optional[Window]:
        if connection:
            if shell and command:
                # change
                xcommand = "/bin/{shell} -l -c {cmd}".format(shell=shell, cmd=command)
                return await iterm2.Window.async_create(connection=connection, command=xcommand)
            else:
                return await iterm2.Window.async_create(connection=connection)


    async def create(self, connection: Connection):
        try:
            app = await iterm2.async_get_app(connection=connection)

            if app:
                current_window = app.current_terminal_window
                assert current_window

                self.window = await self.__connect(
                                        shell=self.__shell,
                                        command=self.__command, 
                                        connection=connection
                                    )
                assert self.window

                new_tab = self.window.current_tab
                assert new_tab

                self.session = new_tab.current_session
                assert self.session

                self.session_id = self.session.session_id
                self.window_id = self.window.window_id

                # change
                # Make this optional flag -- name window
                if self.__name:
                    await self.set_window_title(window=self.window, name=self.__name)
                    await self.set_session_name(session=self.session, name=self.__name)

                # used to not change focus to the new window
                if self.__focus:
                    await current_window.async_activate()

        # !TODO
        except Exception as e:
            print(':::::::::::::::::::::::::::::::::::::::')
            print(':::::::::::::::::::::::::::::::::::::::')
            print(':::::::::::::::::::::::::::::::::::::::')
            print(':::::::::::::::::::::::::::::::::::::::')
            print(':::::::::::::::::::::::::::::::::::::::')
            print(repr(e))


def spawn_terminal(
    name: str,
    focus: Optional[bool],
    shell: Optional[str] = None,
    command: Optional[str] = None,
) -> Terminal:
    terminal = Terminal(name=name, focus=focus, shell=shell, command=command)

    iterm2.run_until_complete(coro=terminal.create, retry=False, debug=True)

    return terminal



# parser = argparse.ArgumentParser(description="spawn iterm2 terminal")

# parser.add_argument("--name", 
#                     type=str, 
#                     help="name of terminal session", 
#                     required=True)

# parser.add_argument("--shell", 
#                     type=str, 
#                     help="terminal shell", 
#                     required=False)

# parser.add_argument("--command", 
#                     type=str, 
#                     help="command to be executed directly after lauch, e.g., htop, ls -a", 
#                     required=False)


# args = parser.parse_args()
# t = Terminal(args.name, args.shell, args.command)
# iterm2.run_until_complete(t.create, False)





