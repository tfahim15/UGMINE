file_name = "imdb"
vlabels, elabels = [], []
file = "GraphData/"+file_name+"/active/output.txt"
for line in open(file).readlines():
    if line[0] == 'v':
        _, _, vlabel = line.split(" ")
        vlabel = int(vlabel)
        if vlabel not in vlabels:
            vlabels.append(vlabel)
    if line[0] == 'e':
        _, _, _, elabel = line.split(" ")
        elabel = int(elabel)
        if elabel not in elabels:
            elabels.append(elabel)


def rand(num):
    import numpy as np
    import matplotlib.pyplot as plt
    mu, sigma = 3., 1.
    s = np.random.normal(mu, sigma, num)
    return s


internal, external = 0, 0
for v1 in vlabels:
    for v2 in vlabels:
        if v1 <= v2:
            for e in elabels:
                external += 1


for line in open(file).readlines():
    if line[0] == 'e':
        internal += 1


internal = rand(internal)
external = rand(external)

i, e = 0, 0


fout = open(file_name+"log.txt", "w")
for v1 in vlabels:
    for v2 in vlabels:
        if v1 <= v2:
            for e in elabels:
                fout.write(str(v1)+" "+str(v2)+" "+str(e)+" "+str(external[e])+"\n")
                e += 1


for line in open(file).readlines():
    if line[0] == 'e':
        fout.write(line.replace("\n", "")+" "+str(internal[i])+"\n")
        i += 1
    else:
        fout.write(line)