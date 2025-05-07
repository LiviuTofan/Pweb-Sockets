from setuptools import setup, find_packages

setup(
    name="go2web",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'go2web=main:main',
        ],
    },
    description="A web utility tool for fetching and parsing web content",
    author="Go2Web Developer",
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)