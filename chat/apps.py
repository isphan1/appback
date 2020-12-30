from django.apps import AppConfig


class ChatConfig(AppConfig):
    name = 'chat'

    def ready(self) -> None:
        import chat.signals
