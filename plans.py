import json
import os

PLANS_FILE = "plans.json"

DEFAULT_PLAN = "20K"


def load_plans():
    if not os.path.exists(PLANS_FILE):
        return {}

    try:
        with open(PLANS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_plans(plans):
    with open(PLANS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            plans,
            f,
            ensure_ascii=False,
            indent=4
        )


def get_plan(guild_id):
    plans = load_plans()

    return plans.get(
        str(guild_id),
        DEFAULT_PLAN
    )


def set_plan(guild_id, plan):
    plans = load_plans()

    plans[str(guild_id)] = plan.upper()

    save_plans(plans)


def has_feature(guild_id, feature):
    plan = get_plan(guild_id)

    basic_features = {
        "ai_chat",
        "memory",
        "minecraft"
    }

    vip_features = {
        "welcome",
        "moderation",
        "custom_commands",
        "ai_channel",
        "advanced"
    }

    if feature in basic_features:
        return True

    if feature in vip_features:
        return plan == "40K"

    return False
