import setuptools

from discovery import __version__

from collections import OrderedDict


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discovery-client",
    version=f"{__version__}",
    author="alexandre menezes",
    author_email="alexandre.fmenezes@gmail.com",
    description="async consul client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://github.com/amenezes/discovery-client",
    packages=setuptools.find_packages(include=["discovery", "discovery.*"]),
    python_requires=">=3.8.*",
    project_urls=OrderedDict((
        ('Documentation', 'https://discovery-client.amenezes.net'),
        ('Code', 'https://github.com/amenezes/discovery-client'),
        ('Issue tracker', 'https://github.com/amenezes/discovery-client/issues')
    )),
    install_requires=["aiohttp>=3.6.2"],
    extras_require={
        "httpx": ["httpx>=0.16.1"],
        "aiocli": ["cleo>=0.7.6"],
        "httpxcli": ["cleo>=0.7.6", "httpx>=0.16.1"],
        "all": ["aiohttp>=3.6.2", "httpx>=0.16.1", "cleo>=0.7.6"],
    },
    setup_requires=["setuptools>=38.6.0"],
    entry_points={"console_scripts": ["discovery=discovery.__main__:application.run [cli]"]},
    keywords=['consul', 'service discovery', 'service catalog'],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: AsyncIO",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Libraries",
    ],
)
