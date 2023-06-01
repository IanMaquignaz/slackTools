import os
from pathlib import Path
from setuptools import setup

module_info = {}
os.path.join(os.path.dirname(__file__))
root = Path(__file__).resolve().parent
with open(str(root / "slackTools" / "__config__.py")) as module_info_file:
    exec(module_info_file.read(), module_info)


# Requirements
with open(str(root / "requirements.txt" )) as module_info_file:
    requirements = module_info_file.read().splitlines()
module_info['__install_requires__'] = requirements

setup(
    # Project
    name=module_info['__project_name__'],
    description=module_info['__description__'],
    version=module_info['__version__'],
    license=module_info['__license__'],
    url=module_info['__url__'],

    # Author
    author=module_info['__author__'],
    author_email=module_info['__author_email__'],

    # Configuration
    packages=module_info['__packages__'],
    install_requires=module_info['__install_requires__'],

    classifiers=[
        'Intended Audience :: Science/Research',
    ],
)
