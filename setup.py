from tool.__init__ import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    description='FishBot-Tool: a tool for FishBot',
    author='小鱼',
    url='https://fishros.com',
    download_url='http://github.com/fishros.com/fishbot_tool',
    author_email='fishros[at]foxmail[dot]com',
    version=__version__,
    license='LICENSE.txt',
    install_requires=[
        'six>=1.9.0',
        'pygments>=2.0.2',
        'prompt_toolkit>=1.0.0,<1.1.0',
        'tabulate>=0.7.5',
        'click>=4.0',
        'py-pretty>=0.1',
        'configobj>=5.0.6',
        'pexpect>=3.3',
        'fuzzyfinder>=1.0.0',
        'ruamel.yaml>=0.15.72',
    ],
    extras_require={
        'testing': [
            'pytest>=2.7.0',
        ],
    },
    entry_points={
        'console_scripts': [
        ]
    },
    packages=['fishbot_tool'],
    package_data={},
    scripts=[],
    name='fishbot-tool',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)