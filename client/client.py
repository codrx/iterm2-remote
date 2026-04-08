
import logging
from dataclasses import dataclass
from typing import Optional, Union

import grpc

from proto import iterm2_remote_pb2
from proto import iterm2_remote_pb2_grpc


@dataclass
class SpawnArgs:
    identifier: str
    focus: bool = False
    shell: str = "zsh"
    command: Optional[str] = None

@dataclass
class SendArgs:
    identifier: str
    request_type: str
    request_content: str


def _spawn_terminal_request(stub, cargs: SpawnArgs):
    return stub.SpawnTerminal(
        iterm2_remote_pb2.SpawnTerminalRequest(
            terminal_name=cargs.identifier,
            focus_term=cargs.focus,
            shell=cargs.shell,
            command=cargs.command
        )
    )


def _send_to_terminal_request(stub, cargs: SendArgs):
    return stub.SendToTerminal(
        iterm2_remote_pb2.SendToTerminalRequest(
            terminal_name=cargs.identifier,
            request_type=cargs.request_type,
            request_content=cargs.request_content
        )
    )

def run_client(cargs: Union[SpawnArgs, SendArgs]) -> bool:
    print("Will try to do something")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = iterm2_remote_pb2_grpc.Iterm2RemoteStub(channel)
        response = None

        match cargs:
            case SpawnArgs():
                response = _spawn_terminal_request(stub=stub, cargs=cargs)

            case SendArgs():
                response = _send_to_terminal_request(stub=stub, cargs=cargs)

            case _:
                print("You messesd something up :(")
                return False
            
    print("Client received:", response.ok)
    return True


# old

# def run():
#     print("Will try to do something")
#     with grpc.insecure_channel("localhost:50051") as channel:
#         stub = iterm2_remote_pb2_grpc.Iterm2RemoteStub(channel)
#         response = spawn_terminal_request(stub)
#     print("Client received:", response.ok)

# if __name__ == "__main__":
#     logging.basicConfig()
#     run()

