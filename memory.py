memory = {}


def get_history(user_id):
    if user_id not in memory:
        memory[user_id] = []
    return memory[user_id]


def add_message(user_id, role, content):
    history = get_history(user_id)

    history.append({
        "role": role,
        "content": content
    })

    if len(history) > 10:
        memory[user_id] = history[-10:]


def clear_history(user_id):
    if user_id in memory:
        memory[user_id] = []


def get_all_memory():
    return memory
