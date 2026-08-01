memory = {}

def add_message(user_id, role, content):
    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append({
        "role": role,
        "content": content
    })

    if len(memory[user_id]) > 10:
        memory[user_id] = memory[user_id][-10:]


def get_history(user_id):
    return memory.get(user_id, [])
