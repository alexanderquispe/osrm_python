from setuptools import setup, find_packages

from osrmareas.version import __version__ as version

setup(
    name='osrmareas',
    version=version,
    description='Routes area with osrm API',
    url='https://github.com/d2cml-ai/drdid',
    author='Jhon Flores',
    license="MIT",
    author_email='fr.jhonk@gmail.com',
    packages=['osrmareas'],
    install_requires=[
        'request', 
        'numpy<=1.24.3',
        'pandas',
		'geopandas',
		'alphashape',
		'shapely',
    ],
    long_description='''
    Using OSRM to create areas and routes within a radius.
    '''
)