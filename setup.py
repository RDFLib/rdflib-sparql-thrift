from setuptools import setup

version = 0.1


config = dict(
    name = 'rdflib-sparql-thrift',
    version = version,
    description = "RDFLib BinaryRDF in Thrift SPARQL Result parser.",
    author = "Gunnar Aastrand Grimnes",
    author_email = "gromgull@gmail.com",
    url = "https://github.com/RDFLib/rdflib-sparql-thrift",
    license = "BSD",
    platforms = ["any"],
    classifiers = ["Programming Language :: Python",
                   "License :: OSI Approved :: BSD License",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Operating System :: OS Independent",
                   ],
    packages = ['rdflib_thrift'],

    entry_points = {
        'rdf.plugins.resultparser': [
            'thrift = rdflib_thrift.result:ThriftResultParser',
        ],

    },
    install_requires = ['rdflib', 'thrift'],
    tests_require = ['nose'],

)

setup(**config)
