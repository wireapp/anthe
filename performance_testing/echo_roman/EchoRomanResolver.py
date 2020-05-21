class EchoRomanResolver:
    @staticmethod
    def can_resolve(data: dict) -> bool:
        return data.get('type') == 'conversation.new_text' and \
               data.get('text') and \
               data.get('text').startswith('You said: ')

    @staticmethod
    def resolve(data: dict):
        pass
