import abc


class FontModelMixin:
    __slots__ = ()
    FONT_NAME = ''

    @abc.abstractmethod
    def draw_text(self, *args, **kwargs):
        raise NotImplementedError
