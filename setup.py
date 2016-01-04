from distutils.core import setup


import codecs
import os.path
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


file_text = read(fpath('t411cli/__init__.py'))

setup(
        name='t411cli',
        version=grep('__version__'),
        description='Lightweight command line interface for T411',
        long_description=read(fpath('README.md')),
        url='https://github.com/Xide/t411cli',
        author='Germain Gau',
        author_email='germain.gau@gmail.com',
        license='',
        packages=['t411cli'],
        entry_points={
            'console_scripts': ['t411=t411cli.t411cli:main'],
        },
        zip_safe=False,
        test_suite='tests',
        install_requires=[
            'requests'
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Programming Language :: Python',
            'Operating System :: Unix'
        ]
)
