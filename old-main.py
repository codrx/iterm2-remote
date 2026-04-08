#!/usr/bin/env python


# do using threads?

"""
    Pip Install:
        iterm2
"""

from typing import Optional
import asyncio
import threading

import iterm2



class Terminal: 

    def __init__(self, shell: str="bash", name: Optional[str]=None, command: Optional[str]=None):
        self.name = name
        self.command = command

        self.__shell = shell
        self.__connection = None
        self.__app = None
        self.__window = None
        self.__session = None

    @property 
    def window(self):
        return self.__window

    @window.setter
    def window(self, window: iterm2.Window):
        self.__window = window

    @property 
    def session(self) -> Optional[iterm2.Session]:
        return self.__session

    @session.setter
    def session(self, session: iterm2.Session):
        self.__session = session

    async def send_text_to_session(self, text: str):
        if self.__session:
            await self.__session.async_send_text(text)

    async def send_command_to_session(self, command: str):
        xcommand = command+"\n"
        if self.__session:
            await self.__session.async_send_text(xcommand)


    async def connect(self) -> Optional[iterm2.Window]:
        if self.__connection:
            if self.command:
                xcommand = "/bin/{shell} -l -c {cmd}".format(shell=self.__shell, cmd=self.command)
                return await iterm2.Window.async_create(self.__connection, command=xcommand)
            else:
                return await iterm2.Window.async_create(self.__connection)


    async def create(self, connection):
        self.__connection = connection

        self.__app = await iterm2.async_get_app(self.__connection)

        if self.__app:
            await self.__app.async_activate()

            window = await self.connect()

            session = window.tabs[0].sessions[0]



class TerminalControl: 

    def __init__(self, shell: str):
        self.__terminals = []
        self.__shell = shell


    def add_terminal(self, term: Terminal) -> bool:
        self.__terminals.append(term)
        return True


    def get_terminal(self, name: str) -> Optional[Terminal]:
        for terminal in self.__terminals:
            if terminal.name == name:
                return terminal
        return None

    async def send_command_to_terminal(self, name: str, command: str):
        terminal = self.get_terminal(name)
        if terminal:
            await terminal.send_command_to_session(command)

    async def send_text_to_terminal(self, name: str, text: str):
        terminal = self.get_terminal(name)
        if terminal:
            await terminal.send_text_to_session(text)

    
    def spawn(self, name: Optional[str]=None, command: Optional[str]=None):
        new_terminal = Terminal(self.__shell, name, command)
        self.add_terminal(new_terminal)
        iterm2.run_until_complete(new_terminal.create, False) 



async def main():
    a = TerminalControl("zsh")
    a.spawn("bob")
    await a.send_command_to_terminal("bob", "htop")


if __name__ == "__main__":
    asyncio.run(main())


