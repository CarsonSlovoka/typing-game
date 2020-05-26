==================
Typing Game
==================

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

DEMO
==========

.. image:: https://raw.githubusercontent.com/CarsonSlovoka/typing-game/master/typing_drop_down/_static/demo/home.png
.. image:: https://raw.githubusercontent.com/CarsonSlovoka/typing-game/master/typing_drop_down/_static/demo/dropdown.png
.. image:: https://raw.githubusercontent.com/CarsonSlovoka/typing-game/master/typing_drop_down/_static/demo/stage.png
.. image:: https://raw.githubusercontent.com/CarsonSlovoka/typing-game/master/typing_drop_down/_static/demo/article.png

More
===========

See the `temp/{language}/doc.html`
