.. |ss| raw:: html

    <strike>

.. |se| raw:: html

    </strike>

==================
Release Note
==================

0.3.0
=========

:NEW-FATURES:
    :DOCUMENT:
        - Create the link of **Edit on Github**
        - Build a Combobox on the navigation bar for **select language**.
        - I import the `disqus`_ such that the user can leave the comment between each page.
        - *Create a link for counts the comment of disqus.*

    :GAME-ARTICLE:
        For now, WPM will as the time pass, doing the update.

        .. note:: WPM display if and only if the length of your typing if greater than 4.

:MODIFY:
    - **Rename the project to follow the convention of PyPI.**  (typing_drop_down → typing_game)

:BUG-FIXES:
    - Fixed a performance issue that made the delay when article is long.


0.2.1
=========

Published to PyPI and Github

0.2.0
=========

:NEW-FATURES:
    - Add cli.py for you can run the game with the command line.
    - Now, you can select the article, its file is defined by the user, and you can set by config. (config.py)
    - Providing more colors on the typed, it has responded to different situations, such as correct, wrong, modify.
    - Add the sign (↘) of the Enter key, which is shown on the screen to let the user know should press the key.

:BUG-FIXES:
    Fix a bug of calculating the error of WPM. In the previous edition, when you make a typo, WPM is still increasing.

:MODIFY:
    - Modify the panel of article games, show the WPM and Accuracy only.

:ISSUES:
    - |ss| When the words is too much, it needs the higher FPS. Otherwise, it will cause a little delay. |se| <-- fixes on `0.3.0`_

0.1.0
=========

:NEW-FATURES:
    - Create an introduction for every game.
    - Create the homepage.
    - Provided a new game mode: Article

:BUG-FIXES:

    - remove the none exists subject on the doc.rst (The trouble starts with the copy and paste.)

:ISSUES:
    :dropdown: The display of text color needs to be strengthened.
    :article: |ss|\There is no chooses to provide you with select the article, which you want to type. |se| <-- added on the `0.2.0`_


0.0.0
=========

Write some basic scripts as draft of the game of typing-dropdown

I was attracted by a video, which introduces how to use Python to build a game of typing-dropdown, so I decide to do it by myself.

:ISSUES:
    - |ss| There is no menu page. |se| <-- added on `0.1.0`_
    - |ss| Does it's possible to provide a game for typing the article? |se| <-- added on `0.1.0`_



.. _disqus: https://disqus.com/