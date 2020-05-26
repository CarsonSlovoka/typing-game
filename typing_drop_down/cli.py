import sys
from pathlib import Path

if 'env path':
    sys.path.insert(0, str(Path(__file__).parent.parent))
    print(str(Path(__file__).parent.parent.parent.absolute()))
    from typing_drop_down import config as default_config
    from typing_drop_down import __version__
    from typing_drop_down.api.utils import after_end
    from typing_drop_down.core import TypingGameApp
    from typing_drop_down.views import PyGameView
    sys.path.remove(sys.path[0])

import inspect
import importlib.machinery
import types
import os
import argparse


def get_config(config_path: Path) -> default_config:
    if config_path is None:
        sys.stderr.write(f'use default config file: {(Path(__file__).parent / Path("config.py")).absolute()}')
        return default_config
    if not config_path.exists() and not config_path.is_file():
        raise FileExistsError(f'{config_path.absolute()}')

    new_config_path = Path(__file__).parent / Path('temp/temp_conf.py')
    new_config_path.parent.mkdir(exist_ok=True)

    # exec(open(config).read())
    org_cwd = os.getcwd()
    with after_end(cb_fun=lambda: [
        os.chdir(org_cwd),  # restore work_dir
    ]) as _:

        os.chdir(str(config_path.parent))
        loader = importlib.machinery.SourceFileLoader('user_setting', str(config_path.resolve()))  # the file extension is not important!
        user_module = types.ModuleType(loader.name)
        loader.exec_module(user_module)  # it's ok for you set breakpoint on your file

        # Solve the problem of the relative path.
        [setattr(user_module, member_name, str(member.resolve())) for member_name, member in inspect.getmembers(user_module) if not member_name.startswith('_') and isinstance(member, Path)]
    return user_module


def build_parser() -> argparse.ArgumentParser:
    main_parser = argparse.ArgumentParser(prog='my_app_set.exe',
                                          formatter_class=argparse.RawTextHelpFormatter)  # allow \n \t ...
    main_parser.add_argument('--version', action='version', version='%(prog)s:' + f'{__version__}')
    main_parser.add_argument('config', type=Path, metavar='CONFIG_FILE',
                             help=f'The path of config, which you can refer to the: {(Path(__file__).parent / Path("config.py")).absolute()}')
    return main_parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    user_config = get_config(args.config)
    PyGameView.HEIGHT = user_config.HEIGHT
    PyGameView.WIDTH = user_config.WIDTH
    TypingGameApp(user_config).start()


if __name__ == '__main__':
    main()
