def is_new_poll(data: dict) -> bool:
    return data.get('type') == 'conversation.poll.new'


def resolve_new_poll(data: dict):
    pass
