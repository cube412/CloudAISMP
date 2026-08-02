import re

def scan_log(log: str):

    report = {}

    report["errors"] = len(re.findall(r"ERROR", log, re.IGNORECASE))
    report["warnings"] = len(re.findall(r"WARN", log, re.IGNORECASE))
    report["exceptions"] = len(re.findall(r"Exception", log, re.IGNORECASE))
    report["failed"] = len(re.findall(r"Failed", log, re.IGNORECASE))

    report["plugins"] = []

    plugins = [
        "LuckPerms",
        "Vault",
        "DiscordSRV",
        "BeautyQuests",
        "PlaceholderAPI",
        "Essentials",
        "EssentialsX",
        "Citizens",
        "DecentHolograms",
        "ProtocolLib",
        "WorldEdit",
        "WorldGuard",
        "CoreProtect",
        "CMI",
        "Multiverse-Core",
        "Geyser",
        "Floodgate",
        "ViaVersion",
        "ViaBackwards",
        "ViaRewind",
        "GrimAC",
        "SkinsRestorer",
        "EconomyShopGUI",
        "XConomy",
        "DeluxeMenus",
        "TAB",
        "ItemsAdder",
        "MythicMobs",
        "ExecutableItems",
        "ExcellentCrates",
        "CrazyCrates",
        "Quests",
        "MMOCore",
        "MMOItems",
        "ModelEngine",
        "Shopkeepers",
        "BlueMap",
        "Spark",
        "Chunky",
        "GSit",
        "LiteBans",
        "FastAsyncWorldEdit"
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

    report["suggestions"] = []

    if report["errors"] > 0:
        report["suggestions"].append("Kiểm tra plugin gây lỗi.")

    if report["warnings"] > 5:
        report["suggestions"].append("Server có nhiều WARNING.")

    if report["health"] < 80:
        report["suggestions"].append("Nên backup server trước khi sửa lỗi.")

    return report
