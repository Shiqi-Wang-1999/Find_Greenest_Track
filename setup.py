from setuptools import setup, find_packages

setup(
    name = "tracknaliser",
    version = "0.1.0",
    py_modules=['tracknaliser'],
    packages = find_packages(),
    # Set the dependencies
    install_requires = ['numpy','matplotlib', 'mock', 'requests'],
    entry_points = {
        'console_scripts': [
            'greentrack = tracknaliser.command:process'  
    ]})
