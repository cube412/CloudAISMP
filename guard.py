import re


def scan_log(log: str):

    report = {}

    report["errors"] = len(re.findall(r"ERROR", log, re.IGNORECASE))

    report["warnings"] = len(re.findall(r"WARN", log, re.IGNORECASE))

    report["exceptions"] = len(re.findall(r"Exception", log))

    report["failed"] = len(re.findall(r"Failed", log))

    report["plugins"] = []

    plugins = [
        "LuckPerms",
        "Vault",
        "DiscordSRV",
        "BeautyQuests",
        "Geyser",
        "ViaVersion",
        "ViaBackwards",
        "ViaRewind",
        "GrimAC",
        "PlaceholderAPI",
        "Essentials",
        "Citizens"
    ]

    for plugin in plugins:

        if plugin.lower() in log.lower():
            report["plugins"].append(plugin)

    health = 100

    health -= report["errors"] * 15
    health -= report["warnings"] * 5
    health -= report["exceptions"] * 10
    health -= report["failed"] * 10

    if health < 0:
        health = 0

    report["health"] = health

    return report
