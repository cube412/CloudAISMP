# =========================
# CloudAI Plans
# =========================

PLANS = {

    "basic": {
        "name": "Basic",
        "price": 20000,

        "features": [
            "AI Chat",
            "Discord Commands",
            "Memory"
        ]
    },

    "vip": {
        "name": "VIP",
        "price": 40000,

        "features": [
            "AI Chat",
            "Discord Commands",
            "Memory",
            "Welcome",
            "Moderation",
            "Custom Personality"
        ]
    },

    "custom": {
        "name": "Custom",
        "price": 50000,

        "features": [
            "AI Chat",
            "Memory",
            "Custom Personality",
            "Custom Commands",
            "Custom Features"
        ]
    }

}


def get_plan(plan_id):

    return PLANS.get(plan_id)


def get_all_plans():

    return PLANS
