import numbers
import time

import rdflib
import rdflib.plugin
from rdflib.plugins.stores.sparqlstore import SPARQLStore

import SPARQLWrapper.Wrapper

SPARQLWrapper.Wrapper._allowedFormats.append('thrift')
SPARQLWrapper.Wrapper._allowedFormats.append('tsv')

rdflib.plugin.register('thrift', rdflib.query.ResultParser, 'rdflib_thrift.result', 'ThriftResultParser')

g = None

def setup():
    global g
    store = SPARQLStore( returnFormat='thrift' )
    g = rdflib.Graph(store, identifier='http://nlg.orbit.ai/graphs/DataGraph')
    g.open('http://localhost:3030/ntb/query')


def test_literal():

    for row in g.query('SELECT ?s ?p ?o WHERE { ?s ?p ?o FILTER(isLiteral(?o)) } LIMIT 1'):
        print row
        assert isinstance(row.o, rdflib.Literal)

def test_numeric():

    for row in g.query('SELECT ?s ?p ?o WHERE { ?s ?p ?o FILTER(isNumeric(?o)) } LIMIT 1'):
        print row
        assert isinstance(row.o.value, numbers.Number)

def test_undefined():

    for row in g.query('SELECT ?s ?p ?o ?x WHERE { ?s ?p ?o FILTER(isLiteral(?o)) } LIMIT 2'):
        assert row.x is None

def test_20000():

    start = time.time()

    res = list(g.query('SELECT ?s ?p ?o ?x WHERE { ?s ?p ?o } LIMIT 20000'))

    print 'thrift', time.time()-start

def test_20000_xml():

    store = SPARQLStore( returnFormat='xml' )
    g = rdflib.Graph(store, identifier='http://nlg.orbit.ai/graphs/DataGraph')
    g.open('http://localhost:3030/ntb/query')

    start = time.time()

    res = list(g.query('SELECT ?s ?p ?o ?x WHERE { ?s ?p ?o } LIMIT 20000'))

    print 'xml', time.time()-start

def test_20000_json():

    store = SPARQLStore( returnFormat='json' )
    g = rdflib.Graph(store, identifier='http://nlg.orbit.ai/graphs/DataGraph')
    g.open('http://localhost:3030/ntb/query')

    start = time.time()

    res = list(g.query('SELECT ?s ?p ?o ?x WHERE { ?s ?p ?o } LIMIT 20000'))

    print 'json', time.time()-start

def test_20000_tsv():

    store = SPARQLStore( returnFormat='tsv' )
    g = rdflib.Graph(store, identifier='http://nlg.orbit.ai/graphs/DataGraph')
    g.open('http://localhost:3030/ntb/query')

    start = time.time()

    res = list(g.query('SELECT ?s ?p ?o ?x WHERE { ?s ?p ?o } LIMIT 20000'))

    print 'tsv', time.time()-start


if __name__ == '__main__':
    setup()
    test_20000()
    test_20000_xml()
    test_20000_json()
    test_20000_tsv()
    test_literal()
    test_numeric()
    test_undefined()
