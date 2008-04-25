"""Create or open the page database
"""

from PyDbLite import Base

db = Base('pages.pdl').create('name','content','admin','nbvisits','created',
    'version','lastmodif',mode="open")
db.create_index('name')
