# coding=utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssm_neo4j",
    version="1.0",
    author="illool",
    author_email="illool@163.com",
    maintainer="illool",
    maintainer_email="illool@163.com",
    description="subgraph structure mining based on neo4j using gSpan algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fangjiegao/ssm_neo4j",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=['py2neo>=4.3.0', 'networkx>=2.4', 'matplotlib>=2.2.2'],

    python_requires='>=3.6',
)

