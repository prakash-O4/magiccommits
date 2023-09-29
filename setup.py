"""Magic Commit is a Python-based automation tool that revolutionizes the Git commit process. It intelligently analyzes code changes and generates concise commit messages, simplifying version control. Install Magic Commit from PyPI with:

pip install magiccommits

Navigate to your project directory and execute:

magiccommits or mc

Magic Commit scans your codebase, crafting meaningful commit messages by default. Experience streamlined version control effortlessly.

For in-depth usage instructions, run:

mc --help

Visit the Magic Commit repository for comprehensive documentation: https://github.com/prakashBasnet3213/magiccommit

Developed by Prakash Basnet, Inspired from [https://github.com/Nutlope/aicommits]"""


from setuptools import setup, find_packages

setup(
    name='magiccommits',
    version='0.4-dev',
    author='Prakash Basnet',
    description="Automate Git commits with Magic Commit: Smart, concise messages generated from code diffs",
    long_description=__doc__,
    keywords=["Git","Commits","Automation", "Code","Version","Control","Productivity","Diffs"],
    include_package_data=True,
    packages=find_packages(exclude=["dist", "build", "*.egg-info"]),
    py_modules= ['magiccommits'],
    install_requires=[
        'click',
        'pyperclip',
        'readchar',
    ],
    entry_points={
        'console_scripts': [
            'magiccommits=magiccommits.main:cli',
            'mc=magiccommits.main:cli'
        ],
    },
)

print(
     """
--------------------------------
Magic Commit installation complete, Enjoy Coding!
--------------------------------
"""
)