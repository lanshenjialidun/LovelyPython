import cStringIO
import tempfile

import k_config,k_utils

class KStringIO:

    def __init__(self):
        self.stringio = cStringIO.StringIO()
        self.getvalue = self.stringio.getvalue
        self.close = self.stringio.close
        self.tell = self.stringio.tell
        self.seek = self.stringio.seek
        self.read = self.stringio.read
        self.tempfile = tempfile.TemporaryFile()

    def _enc(self, buffer):
        "encode buffer using specified encoding, if it is unicode string"
        if k_config.outputEncoding and isinstance(buffer, unicode):
            buffer = buffer.encode(k_config.outputEncoding, 'xmlcharrefreplace')
        return buffer

    def write(self, s):
        self.stringio.write(self._enc(s))

    def flush(self):
        """Added by Henk Jansen for compatibility"""
        self.stringio.flush()
    
    def fileno(self):
        """Used to avoid exceptions when fileno() is called"""
        return self.tempfile.fileno()