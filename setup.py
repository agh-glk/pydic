from distutils.core import setup

setup(
    name='pydic',
    version='1.2',
    packages=['pydic'],
    url='',
    license='MIT',
    author='Krzysztof Dorosz',
    author_email='cypreess@gmail.com',
    description='Python inflectional dictionary',
    install_requires=['marisa-trie'],
    scripts=[
        'pydic/pydic_create.py',
        'pydic/pydic_stemmer.py',
        'scripts/clp2pydic',
        'scripts/sjp2pydic.py',
    ],
)
