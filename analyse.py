import numpy as np
L = []
cnt = 0
with open('./centers_false', 'r') as file:
    for line in file:
        tuple_str = line.strip()  
        if tuple_str !=  str((-1, -1)):
            cnt += 1

        else:

            if cnt!= 0:
                L.append(cnt)
            cnt = 0
    


L = np.array(L)
print(np.mean(L))
print(np.std(L))
print(np.max(L))