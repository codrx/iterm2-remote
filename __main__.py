
import argparse
from argparse import Namespace

from iterm2_api.actions.spawn import spawn_terminal
from iterm2_api.actions.send import send_to_terminal


"""

    Ignore

"""

def parse_args() -> Namespace:

    parser = argparse.ArgumentParser(description="Somewhat control iterm2 through terminal.")

    subparser = parser.add_subparsers(help="commands", dest="sub")

    # Persist Flag
    parser.add_argument("--persist", "-p", action="store_false", required=False)

    # Quit Persist -- improve
    subparser.add_parser("quit", help="quit pesist mode")

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

    spawn.add_argument("--shell", type=str, help="terminal shell", required=False)

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
    send_g1.add_argument(
        "--id", type=str, help="id of terminal session.", required=False
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


def run(args: Namespace):
    match args.sub:
        case "spawn":
            spawn_terminal(args.name, args.focus, args.shell, args.command)
        case "send":
            send_to_terminal(args.name, args.id, args.command, args.text)
        case _:
            print("There is an error somewhere over the rainbow")


if __name__ == "__main__":
    args = parse_args()
    run(args)

