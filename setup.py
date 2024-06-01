from setuptools import setup, find_packages

setup(
    name='kings_pokeapi',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
    ],
    author="K I N G",
    author_email="your.email@example.com",
    description="A package to scrape Pokemon data",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Sachin-M-at-git/kings_pokeapi.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
