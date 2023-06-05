from setuptools import setup, find_packages

setup(
    name='pymongo_wrapper',
    version='0.1',
    author='MDevPro',
    author_email='mdevpro.2020@gmail.com',
    description='schemaless pymongo wrapper to make the advance mongodb query based on the pymongo package',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'django',
    ],
)
