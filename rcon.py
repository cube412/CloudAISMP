from mcrcon import MCRcon
from config import RCON_HOST, RCON_PORT, RCON_PASSWORD


def run(command):

    try:
        with MCRcon(
            RCON_HOST,
            RCON_PASSWORD,
            port=RCON_PORT
        ) as mcr:

            return mcr.command(command)

    except Exception as e:
        return f"Lỗi RCON: {e}"
