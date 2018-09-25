
def de_norm(value,m):
    min = m[0];max = m[1]
    return value*(max-min)

def de_norm_all(list,m):
    tmp = [de_norm(x, m) for x in list]
    return tmp

def large_than_0(list):
    new_list = []
    for i in list:
        if i < 0:
            new_list.append(0)
        else:
            new_list.append(i)
    return new_list
