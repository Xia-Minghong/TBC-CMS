from django.core.serializers.json import Serializer as Builtin_Serializer

class Serializer(Builtin_Serializer):
    def get_dump_object(self, obj):
        return self._current