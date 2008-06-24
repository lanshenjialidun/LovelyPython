mylist=["a","b","c"]
for index,obj in enumerate(mylist):
    print index,obj
    
print "map(lambda x:x*2,[1,2,3,4,5]) -> ",map(lambda x:x*2,[1,2,3,4,5])

print "zip([1,2,3],[4,5,6]):"
for x,y in zip([1,2,3],[4,5,6]):
    print "x,y",x,y

print "filter(lambda x:x>3,[1,2,3,4,5]) -> ",filter(lambda x:x>3,[1,2,3,4,5])
