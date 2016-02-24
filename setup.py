try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = '1.0.0'
exec(open('t411cli/version.py').read())

setup(
        name='t411cli',
        version=__version__,
        description='Lightweight command line interface for T411 (french torrent website)',
        long_description='Documentation is available `here <https://github.com/Xide/t411cli/blob/master/README.md>`_',
        url='https://github.com/Xide/t411cli',
        author='Germain Gau',
        author_email='germain.gau@gmail.com',
        license='THE BEER-WARE LICENSE',
        packages=['t411cli'],
        entry_points={
            'console_scripts': ['t411=t411cli.t411cli:main'],
        },
        zip_safe=False,
        test_suite='tests',
        install_requires=[
            't411api>=0.1.4',
            'colorama'
        ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: End Users/Desktop',
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Programming Language :: Python',
            'Operating System :: Unix'
        ]
)
