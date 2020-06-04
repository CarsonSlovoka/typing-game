.. raw:: html

    <p align="left">

        <a href="https://pypi.org/project/typing-game/">
        <img src="https://img.shields.io/static/v1?&style=plastic&logo=pypi&label=App&message=typing-game&color=00FFFF"/></a>

        <a href="https://pypi.org/project/carson-tool.typing-gameTW/">
        <img src="https://img.shields.io/pypi/v/typing-game.svg?&style=plastic&logo=pypi&color=00FFFF"/></a>

        <a href="https://pypi.org/project/typing-game/">
        <img src="https://img.shields.io/pypi/pyversions/typing-game.svg?&style=plastic&logo=pypi&color=00FFFF"/></a>

        <a href="https://github.com/CarsonSlovoka/typing-game/blob/master/LICENSE">
        <img src="https://img.shields.io/pypi/l/typing-game.svg?&style=plastic&logo=pypi&color=00FFFF"/></a>

        <br>

        <a href="https://github.com/CarsonSlovoka/typing-game">
        <img src="https://img.shields.io/github/last-commit/CarsonSlovoka/typing-game?&style=plastic&logo=github&color=00FF00"/></a>

        <img src="https://img.shields.io/github/commit-activity/y/CarsonSlovoka/typing-game?&style=plastic&logo=github&color=0000FF"/>

        <a href="https://github.com/CarsonSlovoka/typing-game">
        <img src="https://img.shields.io/github/contributors/CarsonSlovoka/typing-game?&style=plastic&logo=github&color=111111"/></a>

        <a href="https://github.com/CarsonSlovoka/typing-game">
        <img src="https://img.shields.io/github/repo-size/CarsonSlovoka/typing-game?&style=plastic&logo=github"/></a>

        <br>

        <a href="https://pepy.tech/project/typing-game">
        <img src="https://pepy.tech/badge/typing-game"/></a>

        <!--

        <a href="https://pepy.tech/project/typing-game/month">
        <img src="https://pepy.tech/badge/typing-game/month"/></a>

        <a href="https://pepy.tech/project/typing-game/week">
        <img src="https://pepy.tech/badge/typing-game/week"/></a>

        -->

        <!--
            <img src="https://img.shields.io/github/commits-since/m/CarsonSlovoka/typing-game/Dev?label=commits%20to%20be%20deployed"/></a>
        -->

    </p>


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

    **conf.py** is defined by yourself. About the contents of ``config.py``, please see `here <https://github.com/CarsonSlovoka/typing-game/blob/release/typing_game/config.py>`_.

an example of conf.py:

.. code-block:: python

    from pathlib import Path

    __this_dir__ = Path(str(Path('.').parent.absolute()))  # do not use the __file__

    # TypingDropDown
    DROPDOWN_TXT = __this_dir__ / Path('words.txt')  # r"C:\\...\words.txt"

    # TypingArticle
    ARTICLE_DIR = __this_dir__ / Path('article')  # The files in which is you want to type.

    WIDTH, HEIGHT = (1600, 600)


.. uml::

    @startmindmap

    *[#Orange] "C:/temp"
    **_ words.txt
    ** article
    ***_ 1.basic.txt
    ***_ 2.level2.txt
    ***_ 100.language.py

    @endmindmap

.. note::

    Each file on the articles, which name should start with a number and use the dot to split the name.

    The file extension can be in any format, not limited to text files.


DEMO
==========

.. image:: https://raw.githubusercontent.com/CarsonSlovoka/typing-game/master/typing_game/_static/demo/home.png
.. image:: https://raw.githubusercontent.com/CarsonSlovoka/typing-game/master/typing_game/_static/demo/dropdown.png
.. image:: https://raw.githubusercontent.com/CarsonSlovoka/typing-game/master/typing_game/_static/demo/stage.png
.. image:: https://raw.githubusercontent.com/CarsonSlovoka/typing-game/master/typing_game/_static/demo/article.png


Contributing
===============

If you want to contribute, please use **release**\'s branch as the main branch,
The **master** branch is just purely used to create a GitHub page.

Be sure to **write tests** for new features. If you have any difficulties, you can ask me or discuss with me. I am glad if you want to join us.

By the way, I'm very friendly!


More
===========

See the `documentation <https://carsonslovoka.github.io/typing-game/>`_
