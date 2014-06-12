from setuptools import setup


version = '1.2'

with open('README.md') as f:
    long_description = f.read()


setup(
    name='magnum-pi',
    version=version,
    description='Builds a python package index out of a directory of packages',
    long_description=long_description,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    keywords='python eggs pypi index package gz tar zip whl wheel',
    author='Ronald Evers',
    author_email='ronald@ch10.nl',
    url='https://github.com/ronaldevers/magnum-pi/',
    license='MIT',
    packages=['magnumpi'],
    entry_points={
        'console_scripts': [
            'makeindex = magnumpi.makeindex:main'
        ],
    }
)
