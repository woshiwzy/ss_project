# -*- coding: utf-8 -*-


def encopyt(input):
    ret = input
    result=""
    for r in ret:
        ri=int(r)
        if ri<= 4:
            x=str( (4 + ri))
            result= result+x
            print "x:", x
        else:
            y=str(9-ri)
            print "y:",y
            result=result+y

    return result


x="666666"
print(":::"+encopyt(x))
