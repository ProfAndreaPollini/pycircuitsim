import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycirctuisim-andreapollini",  # Replace with your own username
    version="0.0.1",
    author="Andrea Pollini",
    author_email="prof.andrea.pollini@gmail.com",
    description="An educational circuit simulator library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ProfAndreaPollini/pycircuitsim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
