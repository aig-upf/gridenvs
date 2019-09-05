from setuptools import setup, find_packages

setup(
    name='gridenvs',
    version='0.1',
    packages=[pkg for pkg in find_packages() if pkg.startswith("gridenvs")],
    keywords='environment, agent, rl, openaigym, openai-gym, gym',
    install_requires=[
        'gym>=0.10.9',
        'numpy>=1.15.4',
        'opencv-python>=3.4.5.20'
    ]
)
