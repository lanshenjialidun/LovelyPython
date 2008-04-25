"""
If the page database doesn't exist, create it
Initialize the variable db
"""

from PyDbLite import Base

db = Base('pages.pdl').create('name','content','admin',
    'nbvisits','created','version','lastmodif',mode="open")
