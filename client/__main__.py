

from client.client import run_client, SpawnArgs, SendArgs


import argparse
from argparse import Namespace

def parse_args() -> Namespace:

    parser = argparse.ArgumentParser(description="Somewhat control iterm2 through terminal.")

    subparser = parser.add_subparsers(help="commands", dest="sub")

    # TODO
    # # Persist Flag
    # parser.add_argument("--persist", "-p", action="store_false", required=False)

    # Quit Persist -- improve
    # subparser.add_parser("quit", help="quit pesist mode")

    # Spawn --- 
    spawn = subparser.add_parser("spawn", help="spawn terminal")

    spawn.add_argument(
        "--name", type=str, help="name of terminal session.", required=True
    )

    spawn.add_argument(
        "--focus",
        "-f",
        help="keep focus on terminal on spawn",
        action="store_false",
        required=False,
    )

    spawn.add_argument("--shell", type=str, help="terminal shell (default is zsh)", required=False)

    spawn.add_argument(
        "--command",
        type=str,
        help="command to be executed directly after lauch, e.g., htop, ls -a",
        required=False,
    )


    # Send ---
    send = subparser.add_parser("send", help="send to terminal") 

    send_g1 = send.add_mutually_exclusive_group(required=True)
    send_g1.add_argument(
        "--name", type=str, help="name of terminal session.", required=False
    )

    # i don't think id is needed
    send_g1.add_argument(
        "--id", type=str, help="id of terminal session. (don't use)", required=False
    )


    send_g2 = send.add_mutually_exclusive_group(required=True)
    send_g2.add_argument(
        "--command",
        type=str,
        help="command to send to terminal to be executed, e.g., htop, ls -a.",
        required=False,
    )
    send_g2.add_argument(
        "--text", type=str, help="text to send to terminal.", required=False
    )

    args = parser.parse_args()

    return args



if __name__ == "__main__":
    args = parse_args()
    cargs = None

    match args.sub:

        case "spawn":

            # too lazy to change more to get default val used for shell
            # don't know how but shell and command options are broken
            # i think all of this broke
            if args.shell:
                cargs = SpawnArgs(identifier=args.name, focus=args.focus, shell=args.shell, command=args.command)
            else:
                cargs = SpawnArgs(identifier=args.name, focus=args.focus, command=args.command)

            run_client(cargs=cargs)

        case "send":
            # there is args.id but i don't think that is used
            identifier = args.name

            request_type = None
            request_content = None
            if args.command:
                request_type = "command"
                request_content = args.command
            else:
                request_type = "text"
                request_content = args.text

            cargs = SendArgs(identifier=identifier, request_type=request_type, request_content=request_content)
            run_client(cargs=cargs)

        case _:
            print("There is an error somewhere over the rainbow")











