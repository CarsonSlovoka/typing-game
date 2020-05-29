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


def init_support_lang_list(
    app: Sphinx, pagename: str, templatename: str,
    context: dict, doctree):

    if templatename != 'page.html':
        return

    context['support_lang_list'] = app.config.support_lang_list


def setup(app: Sphinx):
    app.add_config_value('support_lang_list', default=['en', ''], rebuild='html')
    app.connect(event='html-page-context', callback=init_support_lang_list)  # https://www.sphinx-doc.org/en/master/extdev/appapi.html
