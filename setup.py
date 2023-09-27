import setuptools

with open('requirements.txt', 'r') as fr:
    REQUIREMENTS = fr.read().split('\n')

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="cli",
    version="0.0.1",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=REQUIREMENTS
)
