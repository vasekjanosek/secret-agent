from setuptools import setup

setup(
    name='game',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'game = game.__main__:main'
        ],
    }
)