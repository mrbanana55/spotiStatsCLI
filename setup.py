from setuptools import setup, find_packages

setup(
    name='spotiStats',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'spotipy',
        'rich',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'spotiStats=spotistats.main:main',
        ],
    },
)
