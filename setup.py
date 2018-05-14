from setuptools import setup, find_packages

# import unittest
# import doctest

# Read in the version number
exec(open('src/opt_mo/version.py', 'r').read())

requirements = ["pandas"]


# def test_suite():
#     """Discover all tests in the tests dir"""
#     test_loader = unittest.TestLoader()
#     # Read in unit tests
#     test_suite = test_loader.discover('tests')

#     # Read in doctests from README
#     test_suite.addTests(doctest.DocFileSuite('README.md',
#                                              optionflags=doctest.ELLIPSIS))
#     return test_suite

setup(
    name='opt_mo',
    version=__version__,
    install_requires=requirements,
    author='Nikoleta Glynatsi',
    author_email=('glynatsine@cardiff.ac.uk'),
    packages=find_packages('src'),
    package_dir={"": "src"},
    description='A package used in the study of memory one strategies.',
)
