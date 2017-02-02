from thrift.transport.TTransport import TTransportBase

class TIOStreamTransport(TTransportBase):

    def __init__(self, input_stream, output_stream=None):
        self.input_stream = input_stream
        self.output_stream = output_stream

    def isOpen(self):
        return True

    def close(self):
        pass

    def read(self, sz):
        return self.input_stream.read(sz)

    def write(self, buf):
        self.output_stream.write(buf)

    def flush(self):
        pass
