from pathlib import Path

__this_dir__ = Path('.').parent  # do not use the __file__

# TypingDropDown
DROPDOWN_TXT = __this_dir__ / Path('words.txt')

# TypingArticle
ARTICLE_DIR = __this_dir__ / Path('article')

WIDTH, HEIGHT = (1600, 600)
