import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()
  
setuptools.setup(
    name="SchoolAPI",
    version="1.0b0",
    author="DavidZhivaev",
    author_email="<zhivaevda.dev@gmail.com>",
    description="Библиотека для удобной разработки проектов, связанных с МЭШ.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DavidZhivaev/SchoolAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    install_requires=['requests', "pydantic"]
)
