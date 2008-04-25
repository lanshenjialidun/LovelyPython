import docutils.core

def wiki_formatter(text):

    publisher = docutils.core.Publisher()
    output = docutils.core.publish_parts(text, writer_name='html')

    out = output['body']
    return out

print wiki_formatter('bla bla bla')