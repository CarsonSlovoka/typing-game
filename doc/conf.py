import pygments.styles
from pathlib import Path

if 'sys path setting':
    import sys
    import os
    if 'source code path':
        code_dir = Path(__file__).parent.parent / Path('typing_drop_down')
        sys.path.insert(0, str(code_dir))  # use for ``.. automodule``
    sys.path.append(str(Path(__file__).parent))  # _static/uml/...
    plantuml = f'java -jar {Path(os.environ["USERPROFILE"]) / Path("plantuml.jar")}'

    sys.path.append(str(Path(__file__).parent.parent))  # _static/uml/...
    from typing_drop_down import __version__

master_file = Path(__file__).parent / Path('doc.rst')
source_dir = Path(__file__).parent
output_path = None  # default Path(master_file).parent.parent / docs / language

master_doc = master_file.stem
project = 'Typing Game'  # project_name
release = __version__  # full_version: x.x.x
version = __version__[:__version__.rfind('.')]  # short_version: x.x
copyright = 'Copyright (c) 2020 Carson'
author = 'Carson Tseng'
language = 'en'  # 'zh_TW' # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language

# source_encoding = 'utf-8-sig' default
source_suffix = ['.rst', '.md']
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.todo',
              'sphinx.ext.mathjax',
              'sphinxcontrib.plantuml',
              ]

todo_include_todos = True
pygments_style = pygments.styles.STYLE_MAP['vim'].split('::')[0]  # https://help.farbox.com/pygments.html  # https://pygments.org/demo/

if 'html setting':
    html_css_files = ['css/user_define.css',
                      'css/pygments.vim.css',
                      'css/themes/rtd.page.css']

    html_show_sourcelink = False  # see: app.config.values
    html_show_sphinx = False
    html_static_path = ['_static', ]  # put the css file at self.master_file.parent/Path(self.HTML_STATIC_PATH)/.../xxx.css
    # html_theme_path = ["_templates"]  # from ``Lib\site-packages\{theme}\`` copy to ``.\_templates/{theme}``  and **theme.conf** must exist!
    html_theme = 'sphinx_rtd_theme'  # 'nature'
    html_theme_options = {  # see Lib\site-packages\{theme}\theme.conf
        # "analytics_id": ""
        "style_nav_header_background": "#4e917a",
    }
    html_favicon = '_static/favicon.png'  # Modern browsers use this as the **icon for tabs**.
    html_logo = '_static/logo.jpg'  # An image file that is the logo of the docs. It is placed at the top of the **sidebar**
    # html_search_language = 'zh'  # language[:2]  # https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_search_language
    html_copy_source = False

if 'localization':
    locale_dirs = ['locale/']  # path is example but recommended.

    if 'my setting':
        support_lang_list = ['en', 'zh_TW']
        get_text_output_dir = Path(__file__).parent / '_gettext'

if 'my setting':
    # LEXERS = dict()  # https://stackoverflow.com/questions/16469869/custom-syntax-highlighting-with-sphinx
    NO_JEKYLL = True  # you need to create an empty file in the root directory that lets GitHub know you aren't using Jekyll to structure your site.
    # RST_EPILOG = '\n'.join([f'..include:: {Path(__file__).parent/Path("_templates/style.define.rst")}'])  <-- not use

    FORCE_REBUILD = False  # write all files (default: only write new and changed files)
