import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydict-cedar",
    version="0.0.3",
    author="Zhanliang Liu",
    author_email="liang@zliu.org",
    description="An updateable dict service for Python3, multi-pattern match",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liuzl/pyd",
    packages=setuptools.find_packages(),
    py_modules=['pydict'],
    install_requires=[
        "lsm-db",
        "pycedar"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
