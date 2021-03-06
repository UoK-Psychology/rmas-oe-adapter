from distutils.core import setup

setup(
    name='RMAS-OE-Adapter',
    version='0.1.3',
    author='Jason Marshall',
    author_email='j.j.marshall@kent.ac.uk',
    packages=['rmas_oe_adapter', 
              'rmas_oe_adapter.handlers', 
              ],
    scripts=['rmas_oe_adapter/bin/rmas_oe_adapter_runner.py'],
    url='http://pypi.python.org/pypi/RMAS-OE-Adapter/',
    license='LICENSE.txt',
    description='A basic framework for building RMAS adapters',
    long_description=open('README.md').read(),
    install_requires=[
        "pymongo == 2.3",
        "requests == 0.14.1",
        "RMASAdapter == 0.1.4 ",
        "pika==0.9.8",
    ],
)
