import rdflib
import rdflib.plugin
from rdflib.plugins.stores.sparqlstore import SPARQLStore

import SPARQLWrapper.Wrapper

SPARQLWrapper.Wrapper._allowedFormats.append('thrift')

rdflib.plugin.register('thrift', rdflib.query.ResultParser, 'rdflib_thrift.result', 'ThriftResultParser')

def test_it():


    store = SPARQLStore( returnFormat='thrift' )
    g = rdflib.Graph(store, identifier='http://nlg.orbit.ai/graphs/DataGraph')
    g.open('http://localhost:3030/ntb/query')

    for row in g.query('SELECT ?s ?o ?x WHERE { ?s rdf:type ?o } LIMIT 2'):
        print row



if __name__ == '__main__':
    test_it()
