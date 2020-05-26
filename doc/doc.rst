.. . :numbered:

====================================================
Typing-Game: Documentation
====================================================

.. contents:: Table of Contents

This is a set of typing-game.

Install
============

``pip install typing-game``

USAGE
------

open the command line:

    ``typing-game config.py``

.. note::

    **conf.py** is defined by yourself. About the contents of ``config.py``, please see `here <https://github.com/CarsonSlovoka/typing-game/blob/master/typing_drop_down/config.py>`_.

an example of conf.py:

.. code-block:: python

    from pathlib import Path

    __this_dir__ = Path('.').parent  # do not use the __file__

    # TypingDropDown
    DROPDOWN_TXT = __this_dir__ / Path('words.txt')

    # TypingArticle
    ARTICLE_DIR = __this_dir__ / Path('article')  # The files in which is you want to type.

    WIDTH, HEIGHT = (1600, 600)



Article
============

Game
------------

.. toctree::
    :caption: typing dropdown
    :glob:
    :maxdepth: 3

    source/game/typing_dropdown/dropdown.index.rst



.. toctree::
    :caption: typing article
    :glob:
    :maxdepth: 3

    source/game/typing_article/article.index.rst

----

.. toctree::
    :caption: Hierarchy
    :glob:
    :maxdepth: 3

    source/hierarchy/*


History
==============

.. toctree::
    :caption: Release note
    :maxdepth: 3

    source/history/release.rst


----

REFERENCE
==============

----

Footnotes
---------

----

Citations
---------

