from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="remote-clipboard-mqtt",
    version="0.1",
    description="A small tool to share your clipboard between multiple machines via a public mqtt server",
    url="",
    author="Balazs Gibizer",
    author_email="gibizer@gmail.com",
    license="Apache License 2.0",
    py_modules=['remote_clipboard'],
    zip_safe=False,
    install_requires=requirements,
    entry_points={
        'console_scripts': ['remote-clipboard=remote_clipboard:main'],
    }
)
