# -*- coding: utf-8 -*-


def encopyt(input):
    ret = input
    result=""
    for r in ret:
        ri=int(r)
        if ri<= 4:
            x=str( (4 + ri))
            result= result+x
        else:
            y=str(9-ri)
            result=result+y

    return result