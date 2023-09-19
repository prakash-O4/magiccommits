from setuptools import setup, find_packages

setup(
    name='magiccommits',
    version='0.0.0',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'click',
        'pyperclip',
    ],
    entry_points={
        'console_scripts': [
            'magiccommits=magiccommits.src.magiccommits:cli',
            'mc=magiccommits.src.magiccommits:cli'
        ],
    },
)