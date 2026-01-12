from setuptools import setup, find_packages

setup(
    name="subway-controller",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "mediapipe",
        "numpy",
        "pynput",
    ],
    entry_points={
        "console_scripts": [
            "subway-controller=src.controller:main",
        ],
    },
    author="Project Team",
    description="An AI-powered gesture-based controller for Subway Surfers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
