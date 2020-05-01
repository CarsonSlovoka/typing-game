class FontProportionalSpacingMixin:
    __slots__ = ()
    FONT_NAME_COMIC_SANS_MS = 'ComicSansMs'


class FontMonoSpacingMixin:
    __slots__ = ()
    FONT_NAME_CONSOLAS = 'Consolas'


class FontNameListMixin(
    FontMonoSpacingMixin,
    FontProportionalSpacingMixin
):
    __slots__ = ()
    # https://docs.microsoft.com/en-us/typography/fonts/windows_10_font_list

    @staticmethod
    def is_proportional_spacing(font_name: str):
        return True if \
            any(
                [font_name == getattr(FontProportionalSpacingMixin, cur_property)
                 for cur_property in dir(FontProportionalSpacingMixin) if not cur_property.startswith('_')]
            ) else False

    @staticmethod
    def is_mono_spacing(font_name: str):
        return True if \
            any(
                [font_name == getattr(FontMonoSpacingMixin, cur_property)
                 for cur_property in dir(FontProportionalSpacingMixin) if not cur_property.startswith('_')]
            ) else False
