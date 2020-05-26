.. |ss| raw:: html

    <strike>

.. |se| raw:: html

    </strike>

==================
Release Note
==================

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
    - When the words is too much, it needs the higher FPS. Otherwise, it will cause a little delay.

0.1.0
=========

Create an introduction for every game.


Strike

    - Create the homepage.
    - Provided a new game mode: Article

:BUG-FIXES:

    - remove the none exists subject on the doc.rst (The trouble starts with the copy and paste.)

:ISSUES:
    :dropdown: The display of text color needs to be strengthened.
    :article: |ss|\There is no chooses to provide you with select the article, which you want to type. |se| <-- added on the 0.2.0


0.0.0
=========

Write some basic scripts as draft of the game of typing-dropdown

I was attracted by a video, which introduces how to use Python to build a game of typing-dropdown, so I decide to do it by myself.

:issue:
    - |ss| There is no menu page. |se| <-- added on 0.1.0
    - |ss| Does it's possible to provide a game for typing the article? |se| <-- added on 0.1.0
