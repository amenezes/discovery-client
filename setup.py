import setuptools

from collections import OrderedDict


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discovery-client",
    version="0.2.3",
    author="alexandre menezes",
    author_email="alexandre.fmenezes@gmail.com",
    description="discovery service client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amenezes/discovery-client",
    packages=setuptools.find_packages(),
    project_urls=OrderedDict((
        ('Documentation', 'https://github.com/amenezes/discovery-client'),
        ('Code', 'https://github.com/amenezes/discovery-client'),
        ('Issue tracker', 'https://github.com/amenezes/discovery-client/issues')
    )),
    extras_require={
        'consul': ['python-consul']
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: AsyncIO",
        "Framework :: Flask",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
