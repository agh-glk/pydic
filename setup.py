from distutils.core import setup

setup(
    name='pydic',
    version='1.0',
    packages=['pydic'],
    url='',
    license='GLK',
    author='Krzysztof Dorosz',
    author_email='cypreess@gmail.com',
    description='Python inflectional dictionary',
    install_requires=['bsddb3'],
    scripts=['pydic/pydic_create.py'],
)
