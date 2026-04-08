
"""

    TODO List: 

        - Peek and Jump
        - ? split class into available script and daemon actions
        - differentiate terminals using colours
        - improve error handling

"""

import logging
import grpc
import asyncio

from concurrent.futures import ThreadPoolExecutor
from typing import DefaultDict

from iterm2_api.helpers.queries import get_all_terminals
from iterm2_api.actions.spawn import spawn_terminal, Terminal
from iterm2_api.actions.send import send_to_terminal

from proto import iterm2_remote_pb2
from proto import iterm2_remote_pb2_grpc


class Iterm2RemoteServer(iterm2_remote_pb2_grpc.Iterm2RemoteServicer):

    def __init__(self):
        self.__running_terminals = get_all_terminals()

        # self.__exec_queue = Queue()
        # self.__queue_not_empty = 0
        


    # # kill itself when no terminals
    # def _unalive(self): 
    #     ...

    def get_running_terminals(self) -> DefaultDict[str, Terminal]:
        return self.__running_terminals

    def show_running_terminals(self):
        print("RUNNING TERMINALS:")
        for k, v in self.__running_terminals.items():
            print(f"{k}: {v}")

    def update_terminal_list(self):

        # get all terminals runs in an async loop
        terminals = get_all_terminals()
        for k, v in terminals.items():
            if v not in self.__running_terminals:
                self.__running_terminals[k] = v 

    def change_terminal_name(self, old_name: str, new_name: str) -> bool:
        if old_name in self.__running_terminals:
            self.__running_terminals[new_name] = self.__running_terminals.pop(old_name)
            return True
        return False


    # RPC method
    def SpawnTerminal(
        self,
        request: iterm2_remote_pb2.SpawnTerminalRequest,
        context: grpc.aio.ServicerContext
    ) -> iterm2_remote_pb2.DoRequestReply:

        # async errors
        # self.update_terminal_list()
    
        terminal_name = request.terminal_name
        focus = request.focus_term
        shell = request.shell
        command = request.command


        # if name is None or not unique
        if terminal_name is None or terminal_name in self.__running_terminals:
            terminal_name = str(len(self.__running_terminals))
        
        if focus is None:
            focus = True

        try:
            # Is there no other option? Change event loop policy instead? I have basic asyncio knowledge...
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop=loop)

            terminal = spawn_terminal(name=terminal_name, focus=focus, shell=shell, command=command)

            print(f"SPAWNED: {terminal_name}  -- id: {terminal.session}")
            self.__running_terminals[terminal_name] = terminal.session

            # make show_running_terminal conditional
            print()
            self.show_running_terminals()
            print()
                    
            return iterm2_remote_pb2.DoRequestReply(ok=True, error=None)

        except Exception as e:
            return iterm2_remote_pb2.DoRequestReply(ok=False, error=repr(e))


    # RPC method
    def SendToTerminal(
        self,
        request: iterm2_remote_pb2.SendToTerminalRequest,
        context: grpc.aio.ServicerContext,
    ) -> iterm2_remote_pb2.DoRequestReply:

        # async errors
        # self.update_terminal_list()

        terminal_name = request.terminal_name
        request_type = request.request_type
        request_content = request.request_content

        message_status = False

        try:
            session_id = self.__running_terminals[terminal_name].session_id

            if request_type == "command":
                message_status = send_to_terminal(session_id=session_id, command=request_content)

            if request_type == "text":
                message_status = send_to_terminal(session_id=session_id, text=request_content)

            return iterm2_remote_pb2.DoRequestReply(ok=message_status, error=None)
            
       
        except Exception as e:
            return iterm2_remote_pb2.DoRequestReply(ok=message_status, error=repr(e))

    # TODO
    # def JumpToTerminal(
    #         self,
    #         request: iterm2_remote_pb2.JumptoTerminalRequest,
    #         context: grpc.aio.ServicerContext
    #     ) -> iterm2_remote_pb2.DoRequestReply:

    #     return iterm2_remote_pb2.DoRequestReply(ok=True, error=None)

    # TODO
    # def PeekTerminal(
    #     self,
    #     request: iterm2_remote_pb2.PeekTerminalRequest,
    #     context: grpc.aio.ServicerContext,
    # ) -> iterm2_remote_pb2.DoRequestReply:

    #     session_name = request.terminal_name
    #     if self.__running_terminals[session_name]:
    #         pass

    #     return iterm2_remote_pb2.DoRequestReply(ok=True, error=None)


def serve():
    port = "50051"
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    iterm2_remote_pb2_grpc.add_Iterm2RemoteServicer_to_server(Iterm2RemoteServer(), server)

    # idk why this is not being printed anymore
    listen_addr = "[::]:" + port
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
