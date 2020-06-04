"""
This script is an old fashioned, but it can teach you how to write the extension.
"""

from pathlib import Path
from typing import Union
import warnings
from sphinx.application import Sphinx
from docutils.nodes import Node
from docutils.nodes import document


def get_github_url(app, mode, path):
    """

    :param app:
    :param mode:  # blob, edit ...
    :param path:
    :return:
    """
    return f'https://github.com/{app.config.edit_on_github_project}/{mode}/{app.config.edit_on_github_branch}/{path}'


def html_page_context(app: Sphinx,
                      pagename: str, templatename: str,
                      context: dict,
                      doctree: Union[document, Node]  # all the elements from the docutils.nodes
                      ):
    """
    StandaloneHTMLBuilder.handle_page -> Sphinx().app.emit_firstresult('html-page-context', pagename, templatename, ctx, event_arg)

    :param app: Sphinx. you can get config by it.
    :param pagename: source_dir + file base name(without suffix) of (rst, md ...) <- that you defined in source_suffix  # ex: source/game/typing_article/article.index
    :param templatename: sphinx.builders.html.__init__.py -> handle_page. it can be page.html, genindex.html...  # also ref: site-packages/sphinx/themes/basic
    :param context:  default values see: sphinx.builders.html StandaloneHTMLBuilder.globalcontext
    :param doctree:
    :return:
    """
    if templatename != 'page.html':
        return

    if not app.config.edit_on_github_project:
        warnings.warn("edit_on_github_project not specified")
        return

    builder_src_dir = app.builder.srcdir
    source_file: str = doctree.get('source')  # your pagename file path.
    source_file_name = Path(source_file).name  # doc.rst, index.res ...
    show_url = get_github_url(app, 'blob', source_file_name)
    edit_url = get_github_url(app, 'edit', source_file_name)

    context['show_on_github_url'] = show_url
    context['edit_on_github_url'] = edit_url


def setup(app: Sphinx):
    app.add_config_value(name='edit_on_github_project', default='', rebuild='html')  # If the third argument was 'html', HTML documents would be full rebuild if the config value changed its value.
    app.add_config_value('edit_on_github_branch', 'master', True)

    # event:
    # from sphinx.events import core_events
    # https://www.sphinx-doc.org/en/master/extdev/appapi.html
    app.connect(event='html-page-context', callback=html_page_context)
