from pathlib import Path
import sys

if 'env path':
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from typing_drop_down.core import TypingDropDown, TypingGameApp
    from typing_drop_down.api.utils import ShowTestDescription
    sys.path.remove(sys.path[0])


# obj = TypingDropDown(Path('words.txt'))
# obj.create_game()


obj = TypingGameApp()
obj.show()
