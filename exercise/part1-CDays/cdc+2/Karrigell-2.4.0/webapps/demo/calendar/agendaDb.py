import PyDbLite

db = PyDbLite.Base('entries.pdl').create('content','begin_time','end_time',
    mode="open")
