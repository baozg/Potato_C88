# -*- coding: utf-8 -*-
#================================================
#
#         Author: baozhigui
#          Email: zhigui.bao@gmail.com
#         Create: 2021-07-29 22:28:59
#    Description: -
#
#================================================
import click
import numpy as np
import pandas as pd
import pprint

pp = pprint.PrettyPrinter(indent=4)

def linkGeno(geno1,geno2):
    newgeno = []
    for i in range(0,geno1.shape[0]):
        if geno1[i] == 2 and geno2[i] >= 2:
            newgeno.append(2)
        elif geno1[i] == 0:
            newgeno.append(0)
        elif geno1[i] == 1 and (geno2[i]==1 or geno2[i] ==2 or geno2[i]==3):
            newgeno.append(1)
        else:
            newgeno.append('NA')
    return newgeno

def linkGeno2(geno1,geno2):
    newgeno = {}
    for i in range(0,geno1.shape[0]):
        comb = str(geno1[i])+","+str(geno2[i])
        if comb not in newgeno.keys():
            newgeno[comb]=1
        else:
            newgeno[comb]+=1
    str1 = '2,0'
    str2 = '0,4'
    c1 = 0
    c2 = 0
    if str1 in newgeno.keys():
        c1 = newgeno[str1]

    if str2 in newgeno.keys():
        c2 = newgeno[str2]
    #pp.pprint(newgeno)
    count = c1 + c2
    return count


def loadgroup(tsv):
    odict = {}
    with open(tsv,'r') as f:
        for line in f:
            newline = line.strip().split('\t')
            odict[newline[1]]=newline[0]
    return odict

@click.command()
@click.option('--target',help="haplotig score")
@click.option('--tsv',help="haplotig group")
@click.option('--query',help="diplotig score")

def main(target,tsv,query):
    """
    r2 of target and query
    """
    dt = pd.read_csv(target,header=None,sep="\t")
    dq = pd.read_csv(query,header=None,sep="\t")
    
    groupd = loadgroup(tsv)
    #pp.pprint(groupd)
    for ind2,row2 in dq.iterrows():
        dipGeno = np.asarray(row2[1:1035])
        cor = []
        for ind1,row1 in dt.iterrows():
            hapGeno = np.asarray(row1[1:1035],dtype=int)
            count = linkGeno2(hapGeno,dipGeno)
            cor.append(count)
        corindex = np.argsort(np.asarray(cor))
        utgindex = np.asarray(dt[0])

        outline=[]
        for i in range(-1,-1034,-1):
            ord = corindex[i]
            lg = groupd[utgindex[ord]]
            if i == -1:
                outline.append(str(utgindex[ord]))
                outline.append(str(cor[ord]))
                outline.append(groupd[utgindex[ord]])
                firstlg = lg
            else:
                if lg != firstlg and lg.split("_")[0] == firstlg.split("_")[0]:
                    outline.append(str(utgindex[ord]))
                    outline.append(str(cor[ord]))
                    outline.append(groupd[utgindex[ord]])
                    break
        alline = '\t'.join(outline)
        print ('{q}\t{t}'.format(q=row2[0],t=alline))

        
if __name__ == "__main__":
    main()
