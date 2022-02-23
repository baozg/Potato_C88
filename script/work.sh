#!/bin/bash

./run.py  ####重新调整marker_50kb_LG.tsv 的格式和LG 的编号 ,生成marker_50kb_LG.new


####utg上的window marker 被定到不同的LG上
./decide_scaf_on_multiple_LG.py
###utg上的window marker，被比对到DM不同chr上
awk '$4!="-" {print $6,$4}' marker_50kb_LG.flt |sort -k 1,1 -k 2n,2 | sort -u |awk '{print $1}' |uniq -c |awk '$1>1 {print $2}' >ctg_with_multiple_DM_chr
awk '$4!="-" {print $6,$4}' marker_50kb_LG.flt |sort -k 1,1 -k 2n,2 |uniq -c >1.txt
cat ctg_with_multiple_DM_chr | while read line; do awk -v ctg=$line '$2~ctg' 1.txt  >> 2.txt; done;
sort -k 2,2 -k 1rn,1  2.txt > ctg_with_multiple_DM_chr
./decide_scaf_on_multiple_LG.py


filter -k s -a A,1 <(awk '{print $6"\t"$1}' marker_50kb_LG.flt2 |sort -u ) <(awk '{print $1"\t"$2}' C88_hifi_utg.fa.len |sort -k 1,1 ) >grouped.utg.len

for i in {1..12}; do for j in {1..4}; do awk -v lg='LG'$i"_"$j '$2~lg {sum +=$4} END {print lg,sum}' grouped.utg.len; done; done;
