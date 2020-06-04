from pathlib import Path

__this_dir__ = Path(str(Path('.').parent.absolute()))  # do not use the __file__

# TypingDropDown
DROPDOWN_TXT = __this_dir__ / Path('words.txt')  # r"C:\\...\words.txt"

# TypingArticle
ARTICLE_DIR = __this_dir__ / Path('article')  # The files in which is you want to type.

WIDTH, HEIGHT = (1600, 600)
