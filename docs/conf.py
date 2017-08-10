# -*- coding: utf-8 -*-

from setuptools_scm import get_version

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.extlinks',
    'reno.sphinxext',
]

releases_debug = True
releases_release_uri = 'https://github.com/blue-yonder/storefact/releases/tag/%s'

extlinks = {'issue': ('https://github.com/blue-yonder/storefact/issues/%s', 'issue')}

source_suffix = '.rst'
master_doc = 'index'
project = u'Store factory for simplekv'
copyright = u'2015-2017 Blue Yonder GmbH'
version = get_version(root='..')

import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

pygments_style = 'trac'
templates_path = ['.']
html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = True
html_sidebars = {
   '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)
html_theme_options = {
}
