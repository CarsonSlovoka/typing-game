"""
What is this script doing?
    This script is using to generate the document of sphinx early period.
    But now, this script is not important anymore, because I decide to back to that doing control with the config,
    so you can use config to satisfied most things, only with rare things you can't do, for example, setup_extra_html.
"""

from pathlib import Path
from sphinx.builders.html import StandaloneHTMLBuilder  # self.globalcontext
import sys
if 'eny path':
    # sys.path
    module = __import__('doc.conf')
    conf = module.conf

import sphinx.config
import sphinx.cmd.build
from sphinx.cmd.build import patch_docutils, docutils_namespace, handle_exception, Sphinx
from os import startfile
from pathlib import Path
from typing import Union
# from doc._ext.plugin_extra_html import setup_extra_html, setup_simple_extra_html
import shutil


def main(master_file: Path, source_dir: Path, output_dir: Path):
    builder = SphinxBuilder(master_file, source_dir, output_dir)
    builder.start()  #


class SphinxBuilder:
    __slots__ = ('source_dir', 'output_dir',
                 'master_file',  # index.rst
                 'master_doc'  # index
                 )
    NO_JEKYLL = conf.NO_JEKYLL  # you need to create an empty file in the root directory that lets GitHub know you aren't using Jekyll to structure your site.
    FORCE_REBUILD = conf.FORCE_REBUILD
    HTML_CSS_FILES = conf.html_css_files
    LANGUAGE = conf.language
    HTML_STATIC_PATH = conf.html_static_path[0]
    BUILD_FORMAT = 'html'

    def __init__(self, master_file: Union[str, Path],
                 source_dir: Path, output_dir: Path):
        if isinstance(master_file, str):
            master_file = Path(master_file)  # C:\...\{index, README}.rst
        if not master_file.is_file():
            raise FileNotFoundError(master_file)

        self.master_file = master_file

        self.source_dir = source_dir
        self.output_dir = self.master_file.parent.parent / Path(f'docs/{self.LANGUAGE}') if output_dir is None else Path(output_dir)
        self.master_doc = master_file.stem  # 'index'
        self.check_css_files()

    def check_css_files(self):
        for css_sub_path in self.HTML_CSS_FILES:
            cur_css = self.master_file.parent / Path(self.HTML_STATIC_PATH) / Path(css_sub_path)
            if not cur_css.exists():
                raise FileNotFoundError(f'Please check the file: {cur_css.absolute()} that exactly exists.')

    @property
    def cmd_list(self):
        return [str(self.source_dir), str(self.output_dir),
                '-b', self.BUILD_FORMAT,
                # '-D', 'extensions=sphinx.ext.autodoc',  # Define, override conf.py
                '-D', f'master_doc={self.master_doc}',
                ] + (['-a'] if self.FORCE_REBUILD else [])  # write all files (default: only write new and changed files)

    def build_main(self, *args):
        print('=' * 50)
        print(' '.join(['sphinx.cmd.build.exe'] + self.cmd_list))

        conf_dir = str(self.source_dir)
        doc_tree_dir = str(self.output_dir / Path('.doctrees'))
        conf_overrides = dict(
            master_doc=self.master_doc,
            # todo_include_todos=True,
            # language=self.LANGUAGE,
            # html_static_path=self.HTML_STATIC_PATH,
            # html_css_files=self.HTML_CSS_FILES,
        )
        status = sys.stdout
        warning = sys.stderr
        error = sys.stderr

        freshenv = False
        warningiserror = False
        tags = []
        verbosity = 0
        jobs = 1
        keep_going = False
        filenames = []
        try:
            with patch_docutils(str(self.source_dir)), docutils_namespace():
                app = Sphinx(str(self.source_dir), conf_dir, str(self.output_dir),
                             doc_tree_dir, self.BUILD_FORMAT, conf_overrides,
                             status, warning, freshenv, warningiserror,
                             tags, verbosity, jobs, keep_going)
                if self.FORCE_REBUILD:
                    # The Force build seems not to real it is. so just in case, I do it by myself.
                    shutil.rmtree(self.output_dir, ignore_errors=True)
                if isinstance(app.builder, StandaloneHTMLBuilder):
                    # setup_simple_extra_html(app)
                    ...
                app.build(self.FORCE_REBUILD, filenames)

                return app.statuscode
        except (Exception, KeyboardInterrupt) as exc:
            # handle_exception(app, self.cmd_list, exc, error)
            import traceback
            print(traceback.format_exc())
            return 2

    def _start_base(self):
        sphinx.cmd.build.main(self.cmd_list)  # this main will call sphinx.cmd.build.build_main
        startfile(Path(self.output_dir) / Path(self.master_doc + '.html'))
        if self.NO_JEKYLL:
            target_path = self.output_dir.parent / Path('.nojekyll')
            if not target_path.exists():
                open(target_path, 'w').close()

    def start(self):
        sphinx.cmd.build.build_main = self.build_main  # override
        self._start_base()


if __name__ == '__main__':
    main(conf.master_file, conf.source_dir, conf.output_path)
