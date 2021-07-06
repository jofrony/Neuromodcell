import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Neuromodcell',# Replace with your own username
    version="0.0.1",
    author="Johanna Frost Nylen",
    author_email="johanna.frost.nylen@ki.se",
    description="Code for optimising for neuromodulation fo single cell NEURON models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['neuromodcell'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
