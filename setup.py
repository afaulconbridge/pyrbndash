from setuptools import setup

setup(
    name="pyrbn",
    version="1.0.0",
    author="Adam Faulconbridge",
    author_email="afaulconbridge@googlemail.com",
    packages=["pyrbndash"],
    description="Web dashboard about Random Boolean Networks.",
    long_description=open("README.md").read(),
    install_requires=["dash-cytoscape", "pyrbn"],
    extras_require={
        "dev": [
            "pytest-cov",
            "flake8",
            "pylint",
            "pip-tools",
            "pipdeptree",
            "pre-commit",
            "snakeviz",
        ]
    },
)
