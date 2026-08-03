import re

players = {}


def check_grim_log(log_line: str):

    if "GrimAC" not in log_line:
        return None

    pattern = r"\] (\w+) failed ([A-Za-z0-9_]+)"

    match = re.search(pattern, log_line)

    if not match:
        return None

    player = match.group(1)
    check = match.group(2)

    if player not in players:
        players[player] = {
            "violations": 0,
            "checks": []
        }

    players[player]["violations"] += 1

    if check not in players[player]["checks"]:
        players[player]["checks"].append(check)

    return {
        "player": player,
        "violations": players[player]["violations"],
        "checks": players[player]["checks"]
    }


def get_player(player):

    return players.get(player)


def get_all_players():

    return players


def clear_players():

    players.clear()
