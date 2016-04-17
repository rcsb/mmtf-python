

def run_length_decode(inArray):
    """A function to run length decode an int array"""
    switch=False
    outArray=[]
    for item in inArray:
        if switch==False:
            thisItem = item
            switch=True
        else:
            switch=False
            outArray.extend([thisItem]*int(item))
    return outArray

def delta_decode(inArray):
    """A function to delta decode an int array"""
    if len(inArray)==0:
        return []
    thisAns=inArray[0]
    outArray = [thisAns]
    for i in range(1,len(inArray)):
        thisAns+=inArray[i]
        outArray.append(thisAns)
    return outArray