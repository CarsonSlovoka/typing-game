from typing_drop_down.api.generics import RGBColor


class TypingGameColorMixin:
    """ Settings of colors."""
    __slots__ = ()

    TYPING_CORRECT_COLOR = RGBColor.GREEN
    TYPING_CUR_POS_COLOR = RGBColor.BLUE
    TYPING_MODIFY_COLOR = RGBColor.YELLOW
    TYPING_ERROR_COLOR = RGBColor.RED
