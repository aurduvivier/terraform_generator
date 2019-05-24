import os

from setuptools import setup, find_packages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_requirements():
    file_path = '{}/requirements.txt'.format(BASE_DIR)
    install_requires = []
    if os.path.isfile(file_path):
        with open(file_path) as f:
            install_requires = f.read().splitlines()
    return install_requires


setup(
    name='terraform_generator',
    version='0.1.0',
    description='Load tf.j2 templates and tfvars files to generate Terraform code.',
    author='aurelienduvivier@rocketmail.com',
    install_requires=get_requirements(),
    packages=find_packages(exclude=['tests', 'tests.*', '*.test.*']),
    entry_points={
        "console_scripts": [
            'terraform_generator = terraform_generator.main:main',
        ]
    },
)
