"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['Dictionary.py']
DATA_FILES = ['cards.sqlite', 'Cards.ui', 'Create.ui', 'Delete_Words.ui',
              'Dictionary.ui', 'learn-words', 'Login_Password.ui', 'Search_Words.ui', 'Dictionary.png',
              'Dictionary_icon.ico']
OPTIONS = {
    'iconfile': 'Dictionary_icon.ico'
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
