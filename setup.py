from setuptools import setup, find_packages

setup(
    name="job-utils",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'jut=jut.cli:main',
        ],
    },
)
