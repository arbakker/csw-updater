from setuptools import setup, find_packages
from configparser import ConfigParser

version = "0.1.dev0"

long_description = "\n\n".join([open("README.md").read(), open("CHANGES.md").read()])


def parse_pipfile(development = False):
    """Reads package requirements from Pipfile."""
    cfg = ConfigParser()
    cfg.read('Pipfile')
    dev_packages = [p.strip('"') for p in cfg['dev-packages']]
    relevant_packages = [
        p.strip('"') for p in cfg['packages'] if "csw-updater" not in p
    ]
    if development:
        return dev_packages
    else:
        return relevant_packages


setup(
    name="csw-updater",
    version=version,
    description="CLI tool for CSW CRUD operations",
    long_description=long_description,
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=["Programming Language :: Python :: 3"],
    keywords=["csw-updater"],
    author="Anton Bakker",
    author_email="anton.bakker@kadaster.nl",
    url="https://github.com/PDOK/csw-updater",
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_pipfile(),
    tests_require=parse_pipfile(True),
    entry_points={
        "console_scripts": [
            "csw_updater = csw_updater.cli:csw_updater_command"
        ]
    },
)
