import io
from setuptools import setup

with open('requirements.txt') as f:
    required = f.readlines()

setup(
    name='golem_run',
    version='0.0.1',
    description='Simple tool to run scripts on golem',
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/VanDavv/golem-run',
    keywords="golem run glm tool python js",
    entry_points={
        'console_scripts': [
            'golem-run=golem_run.__init__:__run_cli__'
        ],
    },
    author='Łukasz Piłatowski',
    author_email='lukasz.pilatowski@golem.network',
    license_files = ('LICENSE',),
    packages=['golem_run'],
    package_dir={"": "src"},  # https://stackoverflow.com/a/67238346/5494277
    install_requires=required,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
