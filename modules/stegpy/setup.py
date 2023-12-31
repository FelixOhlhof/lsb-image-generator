import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stegpy",
    version="0.0.1",
    author="dhsdshdhk",
    description="A program for encoding information in image and audio files through steganography.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhsdshdhk/stegpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "stegpy=stegpy.steg:main",
        ],
    },
    python_requires=">=3",
    install_requires=["numpy", "cryptography", "Pillow"],
)
