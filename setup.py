from setuptools import setup, find_packages

setup(
    name='pyifs',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python Iterated Function plotter',
    long_description=open('README.md').read(),
    install_requires=['numpy'],
    url='https://github.com/jmbhughes/pyifs',
    author='J. Marcus Hughes',
    author_email='hughes.jmb@gmail.com'
)




