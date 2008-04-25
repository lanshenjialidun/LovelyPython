"""Copy the uploaded file on the script directory"""
import os
print "uploading file %s" %_myfile.filename

# uncomment the following lines to copy the uploaded file 
# to the current directory

"""
f = _myfile.file # file-like object
dest_name = os.path.basename(_myfile.filename)
out = open(dest_name,'wb')
# copy file
import shutil
shutil.copyfileobj(f,out)
out.close()
"""
