from setuptools import setup, find_packages

setup(
    name='bsky_terminal',
    version = '0.0.1',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'Click',
        'atproto'
    ],
    entry_points = {
        'console_scripts':[
            'main = main:cli' 
        ],
    },
)