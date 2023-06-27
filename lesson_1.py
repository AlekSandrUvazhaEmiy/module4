a='abafsdaffasfcdf'
'''''
def ctr(s):
    c = 0
    for sym in s:
        c += 1
    print(c)

ctr(a)
  

def ctr(s):
    for sym in set(s):
        c = 0
        for s_c in s:
            if sym == s_c:
                c += 1 
        print(sym, c)

ctr(a)
'''''

def ctr (s):
    s_c = {}
    for sym in s:
        if sym not in s_c:
            s_c[sym] = 1
        else:
            s_c[sym] += 1
    for sym, c in s_c.items():
        print(sym, c)

ctr(a)