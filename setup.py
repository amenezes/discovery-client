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
    python_requires=">=3.6.0",
    project_urls=OrderedDict((
        ('Documentation', 'https://discovery-client.amenezes.net'),
        ('Code', 'https://github.com/amenezes/discovery-client'),
        ('Issue tracker', 'https://github.com/amenezes/discovery-client/issues')
    )),
    install_requires=[
        "aiohttp<=3.6.2",
    ],
    extras_require={
        "aio": ["aiohttp<=3.6.2"],
        "httpx": ["httpx>=0.12.0"],
        "all": ["aiohttp<=3.6.2", "httpx>=0.12.0"],
    },
    setup_requires=["setuptools>=38.6.0"],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
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
