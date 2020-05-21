def is_execute_command(data: dict) -> bool:
    return data.get('type') == 'conversation.new_text' and \
           data.get('text') and \
           data.get('text').startswith('/execute')


def resolve_execute_command(data: dict):
    pass
