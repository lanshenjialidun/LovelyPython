"""Copy the uploaded file on the script directory"""
import os

def index(**kw):

    print "uploading file %s" %_myfile.filename

    # uncomment the following lines to copy the uploaded file 
    # to the current directory
    
    f = _myfile.file # file-like object
    dest_name = os.path.basename(_myfile.filename)
    print f.read()
