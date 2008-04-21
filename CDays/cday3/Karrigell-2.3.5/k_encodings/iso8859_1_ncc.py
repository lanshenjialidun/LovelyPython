""" Python Character Mapping Codec
Like iso8859_1.py, but does not consider control codes to be valid characters
"""#"

import codecs

### Codec APIs

class Codec(codecs.Codec):

    def encode(self,input,errors='strict'):

        return codecs.charmap_encode(input,errors,encoding_map)

    def decode(self,input,errors='strict'):

        return codecs.charmap_decode(input,errors,decoding_map)

class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

### encodings module API

def getregentry():

    return (Codec().encode,Codec().decode,StreamReader,StreamWriter)

### Decoding Map

decoding_map = codecs.make_identity_dict(range(32, 128)+range(128+32, 256))
decoding_map.update({
})

### Encoding Map

encoding_map = codecs.make_encoding_map(decoding_map)

def _registry(encoding):
    if encoding != 'iso8859_1_ncc':
        return None
    return getregentry()
