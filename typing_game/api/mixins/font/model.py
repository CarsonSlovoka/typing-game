import abc


class FontModelMixin:
    __slots__ = ()

    @abc.abstractmethod
    def draw_text(self, *args, **kwargs):
        raise NotImplementedError
