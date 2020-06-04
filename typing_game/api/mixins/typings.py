# from time import time
from timeit import default_timer  # default_timer() measures wall clock time, not the CPU time
from typing import Generator, Tuple, Union


class StatisticianMixin:
    """
    WPM, CPM,
    """

    __slots__ = ()

    @staticmethod
    def generator_pm_info() -> Generator[Tuple[int, int], Union[int, bool], None]:
        while 1:
            t_s = default_timer()
            total_chars = yield 0, 0
            while 1:
                if isinstance(total_chars, bool) and total_chars is True:  # reset
                    break
                cpm = int(60*total_chars/(default_timer()-t_s))
                wpm = int(cpm/5)
                total_chars = yield cpm, wpm
