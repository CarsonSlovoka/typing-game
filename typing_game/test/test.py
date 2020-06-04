__all__ = ('test_setup',)

import unittest
from unittest import TestCase
from pathlib import Path
import sys
import os
import shutil
import textwrap


if 'env path':
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from typing_drop_down.core import TypingDropDown, TypingGameApp
    from typing_drop_down.api.utils import ShowTestDescription
    from typing_drop_down import config as default_config
    from typing_drop_down.cli import get_config
    from typing_drop_down.cli import main as cli_main
    from typing_drop_down.api.utils import after_end
    sys.path.remove(sys.path[0])


class SingleGameTests(TestCase):
    def test_dropdown_game_is_work(self):
        obj = TypingDropDown(Path('words.txt'))
        obj.start_game()


class IntegrateTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.app = TypingGameApp()

    def test_run_app(self):
        with self.assertRaises(SystemExit) as result:
            TypingGameApp(default_config).start()
        self.assertEqual(result.exception.code, 1)

    def test_run_app_with_config(self):
        # Simulate the behavior that the user provides its config file.
        temp_dir = Path(os.environ.get('Temp')) / Path('typing-drop-down-test')
        (temp_dir/Path('article')).mkdir(parents=True, exist_ok=True)

        new_conf_content = textwrap.dedent(  # Remove any common leading whitespace from every line in text.
            """\
            from pathlib import Path
            __this_dir__ = Path('.').parent
            
            # TypingDropDown
            DROPDOWN_TXT = __this_dir__ / Path('words.txt')
            
            # TypingArticle
            ARTICLE_DIR = __this_dir__ / Path('article')
            """)
        # build the user config
        config_path = temp_dir/Path('temp.conf.py')
        with open(config_path, 'w') as config_file, \
            open(temp_dir/Path('words.txt'), 'w') as words_file, \
            open(temp_dir/Path('article/aaa.txt'), 'w') as article_file:
            config_file.write(new_conf_content)
            words_file.write('aaabbbccc')
            article_file.write('article')

        # get the user config
        with after_end(lambda: shutil.rmtree(temp_dir)) as _:
            config = get_config(config_path)

            # run the app
            with self.assertRaises(SystemExit) as result:
                TypingGameApp(config).start()
            self.assertEqual(result.exception.code, 1)


class CLITests(ShowTestDescription):
    def test_show_version(self):
        with self.assertRaises(SystemExit) as context_manager:
            cli_main(['--version'])
        self.assertEqual(context_manager.exception.code, 0)

    def test_show_help(self):
        with self.assertRaises(SystemExit) as context_manager:
            cli_main(['--help'])
        self.assertEqual(context_manager.exception.code, 0)


def test_setup():
    suite_list = [unittest.TestLoader().loadTestsFromTestCase(class_module) for class_module in (CLITests, )]
    suite_class_set = unittest.TestSuite(suite_list)

    # suite_function_set = unittest.TestSuite()
    # suite_function_set.addTest(module.class('fun_name'))

    suite = suite_class_set  # pick one of two: suite_class_set, suite_function_set
    # unittest.TextTestRunner(verbosity=1).run(suite)  # self.verbosity = 0  # 0, 1, 2.  unittest.TextTestResult
    return suite
