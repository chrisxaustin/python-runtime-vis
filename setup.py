from setuptools import setup, find_packages

setup(
    name="runtime_vis",
    author="Chris Austin",
    url="https://github.com/chrisxaustin/python-runtime-vis",
    version="0.11",
    packages=find_packages(),
    install_requires=[
        "seaborn==0.13.2",
        "pandas==2.2.2",
        "matplotlib==3.9.2",
        "scipy==1.14.1",
    ]
)