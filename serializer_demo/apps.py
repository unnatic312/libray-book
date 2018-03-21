from django.apps import AppConfig


class SerializerDemoConfig(AppConfig):
    name = 'serializer_demo'

    def ready(self):
        import serializer_demo.signal