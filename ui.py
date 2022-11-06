# gui imports
from os import get_terminal_size
from platform import system
from rich.align import Align
from rich.panel import Panel
from rich.text import Text

def get_terminal_width() -> int:
    try:
        width, _ = get_terminal_size()
    except OSError:
        width = 80

    if system().lower() == "windows":
        width -= 1
    return width

def print_banner() -> Panel:
    width = get_terminal_width()
    height = 10
    banner = '''\

    ███████╗██████╗  ██████╗ ████████╗██╗███████╗██╗   ██╗██████╗ ██╗     
    ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝██╔══██╗██║     
    ███████╗██████╔╝██║   ██║   ██║   ██║█████╗   ╚████╔╝ ██║  ██║██║     
    ╚════██║██╔═══╝ ██║   ██║   ██║   ██║██╔══╝    ╚██╔╝  ██║  ██║██║     
        ███████║██║     ╚██████╔╝     ██║   ██║██║        ██║   ██████╔╝███████╗
        ╚══════╝╚═╝       ╚═════╝    ╚═╝   ╚═╝╚═╝        ╚═╝   ╚═════╝ ╚══════╝
'''

    banner_small = """\
░▄▀▀▒█▀▄░▄▀▄░▀█▀░█▒█▀░▀▄▀░█▀▄░█▒░
▒▄██░█▀▒░▀▄▀░▒█▒░█░█▀░▒█▒▒█▄▀▒█▄▄
"""

    if width < 90:
        banner = banner_small
        height = 5

    panel = Panel(
        Align(
            Text(banner, justify="center", style="green"),
            vertical="middle",
            align="center",
        ),
        width=width,
        height=height,
        subtitle="by Balduzz (https://github.com/Bbalduzz)",
    )
    return panel

def leave_msg() -> Panel:
    msg = '[bold green]SpotifyDL[bold green] stopped'
    stop_msg = Panel(
        Align(
            Text(msg, justify="center", style="green"),
            vertical="middle",
            align="center",
        )),
    return stop_msg




