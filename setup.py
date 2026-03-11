"""
This is a setup file for the Network Security System.
it is an essntial part of packaging and distributing python project.
it is used by setuptools (or distutils in older Python versions) to define the configuration
of ur project such as its metadata , dependencies and more
"""

from setuptools import find_packages, setup

from typing import List

def get_requirements() -> List[str]:
    """This function will return the list of requirements"""
    requirements_list: List[str] = []
    try :
        with open('requirements.txt','r') as file :
            lines = file.readlines()
            for line in lines :
                requirement = line.strip()
                if requirement and requirement != "-e ." :
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt not found")
    return requirements_list

## -e . use to refer to the setup.py file and run the entrie code of setup.py file
## it is used to install the project in editable mode(development mode)

setup(
    name = "Network Security System",
    version = "0.0.1",
    author = "Nihar Kedia",
    author_email = "kedianihar852@gmail.com ",
    packages = find_packages(),
    install_requires = get_requirements(),
)
