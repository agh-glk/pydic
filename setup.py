from distutils.core import setup

setup(
    name='pydic',
    version='1.1',
    packages=['pydic'],
    url='',
    license='MIT',
    author='Krzysztof Dorosz',
    author_email='cypreess@gmail.com',
    description='Python inflectional dictionary',
    install_requires=['bsddb3', 'marisa-trie'],
    scripts=[
        'pydic/pydic_create.py',
        'pydic/pydic_stemmer.py',
        'scripts/clp2pydic',
        'scripts/sjp2pydic',
    ],
)
