
from rdflib import Literal, URIRef, BNode, Graph, Variable
from rdflib.query import (
    Result,
    ResultParser,
    ResultSerializer,
    ResultException
)

from thrift.transport.TTransport import TMemoryBuffer
from thrift.protocol.TCompactProtocol import TCompactProtocol

from .ttypes import RDF_VarTuple, RDF_DataTuple, RDF_Term
from .iotransport import TIOStreamTransport

"""A Parser for SPARQL results in Thrift:

http://afs.github.io/rdf-thrift/rdf-compact-thrift.html

"""


class ThriftResultParser(ResultParser):

    def parse(self, source):
        return ThriftResult(source)


class ThriftResult(Result):
    def __init__(self, source):
        super(ThriftResult, self).__init__('SELECT')

        #transport = TIOStreamTransport(source)
        transport = TMemoryBuffer(source.read())
        protocol = TCompactProtocol(transport)

        # t = RDF_Term()
        # t.read(protocol)
        # print t

        _vars = RDF_VarTuple()
        _vars.read(protocol)

        self.vars = [ Variable(v.name) for v in _vars.vars ]

        self.bindings = self._read_and_convert(protocol)

    def _read_and_convert(self, protocol):

        while True:
            try:
                row = RDF_DataTuple()
                row.read(protocol)

                yield { v:self._convert(term) for v,term in zip(self.vars, row.row) }
            except EOFError:
                break

    def _convert(self, term):

        if term.iri:
            return URIRef(term.iri.iri)
        elif term.literal:
            return Literal(term.literal.lex, datatype=term.literal.datatype)
        elif term.undefined:
            return None
        else:

            # TODO: repeat, variable, any, prefixName, valDecimal, valInteger, valDouble

            raise Exception('Could not convert Thrift term: %s'%term)
