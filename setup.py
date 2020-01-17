from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="travelplanner", # Replace with your own username
    version="0.0.4",
    author="Miguel Lopez",
    author_email="miguel.birbuet.19@ucl.ac.uk",
    description="A travel planner package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('travelplanner'),#exclude=['*test']),
    package_dir={'':'travelplanner'}
    install_requires=['numpy','pandas','pytest','matplotlib'],
    entry_points={
        'console_scripts': [
            'bussimula = travelplanner.command:process'
            ]}
)