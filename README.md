# Autotetraploid potato: Cooperation-88 🥔

By leveraging the state-of-the-art sequencing technologies and polyploid graph binning, we achieved a chromosome-scale, haplotype-resolved genome assembly of a cultivated potato, Cooperation-88 (C88).


## Pipeline overview ⚙️
- Hifiasm preliminary assembly
- Classification of utg
- Haplotype-aware genetic phasing
- Polyploidy graph binning of hifiasm
- HiC scaffolding and remove artifact

## Step by step

### Step1 Hifiasm preliminary assembly
```bash
hifiasm -t 64 -o C88 -l 0 --primary C88.HiFi.fa.gz
gfatools gfa2fa C88.p_utg.gfa > C88.p_utg.fa
```
### Step2 Remapping HiFi reads to utg for classification
Based on the coverage of 50kb window, divided the window into five utg type (haplotigs,diplotigs,triplotigs,tetraplotigs and repeat region).
```bash
minimap2 -ax map-hifi C88.p_utg.fa C88.HiFi.fa.gz -t 64|samtools view -@ 64 -Sb -|samtools sort -o C88.hifi.sorted.bam -@ 32 -
samtools index -@ 32 C88.hifi.sorted.bam
mosdepth -t 12 -b 50000 -Q 1 -F 3840 C88_50kb C88.hifi.sorted.bam
perl script/class_utg.pl C88_50kb.regions.bed.gz 30 > result/03.genotype/mosdepth.bed
```
### Step3 Mapping S1 population reads to utg
```bash
ln -s C88.p_utg.fa ref/C88.fa
bwa index ref/C88.fa
samtools faidx ref/C88.fa
cut -f1,2 ref/C88.fa.fai > ref/C88.genome.size
python script/01_scaf_2_window.py C88.genome.size 50000 C88_50kb.windows.id

for s in `cat samples.list`;
do 
  bwa mem -M -R "@RG\tID:${s}\tSM:${s}\tPL:ILLUMINA" -t 8 ref/C88.fa {input.gz1} {input.gz2}| samtools view -@ 8 -Sb - | amtools sort -@ {threads} -o {output.bam} - 
  samtools view -q 1 -F 3840 {input.bam}|python script/02_reads_num_window.py ref/C88_50kb.windows.id {output.readnum} 1 > 01.readnum/${s}.readnum
done

perl script/merge_all_samples_readnum.pl samples.list result/01.mapping/mosdepth.bed ref/C88_50kb.windows.id ./result/02.readnum > result/03.genotype/C88.readnum

# filter by missing rate 
python script/03_contig_filter.py result/03.genotype/C88.readnum result/03.genotype/C88.readnum.flt.matrix
```

### Step4 Haplotype-aware Genetic Mapping
Since HiC phasing cannot work in the collapsed region, we use genetic grouping for phasing.

```bash

mkdir -p haplotig diplotig triplotig

grep -P "_haplotig" result/03.genotype/C88.readnum.flt.matrix > result/03.genotype/haplotig/haplotig.readnum.flt.matrix
grep -P "_diplotig" result/03.genotype/C88.readnum.flt.matrix > result/03.genotype/diplotig/diplotig.readnum.flt.matrix
grep -P "_triplotig" result/03.genotype/C88.readnum.flt.matrix > result/03.genotype/triplotig/triplotig.readnum.flt.matrix



# haplotigs or repeat (same as diploid, 012 score)
## readnum to score

cd result/03.genotype/haplotig/
p="haplotig"
Rscript script/04_peaks_x_y_hist_win.R $p.readnum.flt.matrix $p.peaks_xy.txt
python script/05_contig_yes_or_no.py $p.peaks_xy.txt $p.readnum.flt.matrix  $p.012_score $p.012.yes_no
awk  -F '\t' '/no/ {for (i=2;i<=NF;i++) printf $i"\t"; printf "\n"}'  $p.012.yes_no > 012_failed.yesno
python script/06_segregation_distortion_marker_yes_or_no.py 012_failed.yesno $p.readnum.flt.matrix  $p.01.score  $p.01.score.yesno
cat $p.012_score $p.01.score >  $p.score

## LepMap3 (12 chromosomes)
perl script/genotype2vcf.pl $p.score vcf.header > C88.vcf
java -cp ~/software/LepMap3/bin ParentCall2 removeNonInformative=0 ignoreParentOrder=1 vcfFile=C88.vcf data=ped.txt > data.call
java -cp ~/software/LepMap3/bin Filtering2 data=./data.call MAFLimit=0.05 missingLimit=0.4 dataTolerance=0.0000001 removeNonInformative=1 > data_filter.callq
java -cp ~/software/LepMap3/bin SeparateChromosomes2 data=data_filter.call sizeLimit=100 numThreads=64 lodLimit=15 distortionLod=1 >map15.nofilt.txt

## 12 chromsomes to 48 haplotypes

perl script/group2LG.pl data_filter.call map15.nofilt.txt > groups.txt
python script/split_LG.py groups.txt ../../C88.filter.readnum C88.48LG.out

## cor for unplaced haplotig marker
python script/10_query_reference_marker_set.py  $p.readnum.flt.matrix $p.48LG.out target.readnum  query.readnum

### Need WGCNA R package for faster cor 
Rscript script/03_target_query_correlation.R query.readnum target.readnum readnum.correlation.out

python script/11_show_strongest_second_correlation.py  query.readnum target.group readnum.correlation.out query.readnum_strongest_cor.xls
awk '$3>=0.7  {if ($4==$7) print $1"\t"$2"\t"$5"\t"$4; else if ($4==$10) print $1"\t"$2"\t"$8"\t"$4; else if ($7==$10) print $1"\t"$5"\t"$8"\t"$7 }' ./query.readnum_strongest_cor.xls  >good.cor.marker


# diplotigs

## copy target.readnum in the haplotig
cp result/03.genotype/haplotig/target.readnum result/03.genotype/diplotig/haplotig.target.score

cd result/03.genotype/diplotig/

## fitPoly genotype
perl script/readnum2fitPoly.pl diplotig.readnum.flt.matrix > diplotig.fitPoly.input.tsv
pigz -p 12 diplotig.fitPoly.input.tsv
Rscript script/fitPoly.R diplotig
perl script/fitPoly2genotype.pl diplotig_scores.dat diplotig_models.dat 4 > diplotig.filter.genotype

## find the collapsed
python script/cor_diplotig.py --target result/03.genotype/haplotig/target.readnum --tsv C88.48LG.out --query diplotig.filter.genotype > diplotig.48LG.tsv


## unplaced diplotig marker
python script/10_query_reference_marker_set.py  $p.readnum.flt.matrix $p.48LG.out target.readnum query.readnum
Rscript script/03_target_query_correlation.R  query.readnum target.readnum readnum.correlation.out
python script/11_show_strongest_second_correlation.py  query.readnum target.group readnum.correlation.out query.readnum_strongest_cor.xls
awk '$3>=0.7  {if ($4==$7) print $1"\t"$2"\t"$5"\t"$4; else if ($4==$10) print $1"\t"$2"\t"$8"\t"$4; else if ($7==$10) print $1"\t"$5"\t"$8"\t"$7 }' ./query.readnum_strongest_cor.xls  >good.cor.marker


# triplotigs
cd result/03.genotype/triplotig

p="triplotig"
Rscript script/04_peaks_x_y_hist_win.R $p.readnum.flt.matrix $p.peaks_xy.txt
python script/05_contig_yes_or_no.py $p.peaks_xy.txt $p.readnum.flt.matrix  $p.012_score $p.012.yes_no
awk  -F '\t' '/no/ {for (i=2;i<=NF;i++) printf $i"\t"; printf "\n"}'  $p.012.yes_no > 012_failed.yesno
python script/06_segregation_distortion_marker_yes_or_no.py 012_failed.yesno $p.readnum.flt.matrix  $p.01.score  $p.01.score.yesno
cat $p.012_score $p.01.score >  $p.score

# 2-geno for marker d
perl complement.pl triplotig.score > triplotig_complement.score
ln -s result/03.genotype/haplotig/target.readnum ./target.score
Rscript script/11_target_query_correlation.R triplotig_complement.score target.score triple.correlation.out
python script/11_show_strongest_second_correlation.py triplotig_complement.score C88_cor_haplotig.48LG.out triple.correlation.out query.readnum_strongest_cor.xls




# combine

```

### Step5 Utg phasing to reads
hifiasm gfa keep the non-contained reads record for each utg, we linked the utg phasing to the reads phasing to reduce the mapping bias.
```bash
perl script/reformat.pl utg.group.xls gfa > C88.hifiasm.binutg.reads.list
```

### Step6 Polyploidy graph binning of hifiasm
[hifiasm-dev](https://github.com/chhylp123/hifiasm/tree/hifiasm_dev_debug, commit b640289b19f38388dbeb9b34e78210afeac2eedc) have devlopmented polypoidy graph binning. It utlized the non-contained reads information during the assembly graph build process. It can correct the phasing error and extend the phase block with overlap information. So you will have a more contiguous assembly than binning reads. It should work on more than tetraploid and HiC phasing information (ex. AllHiC pipeline)

```bash
hifiasm -t 64 -o C88 -5 C88.hifiasm.binutg.reads.list --n-hap 4 --hom-cov 120 C88.HiFi.fa.gz
```
`-5` represent the phase information (below), the collapsed region will use the reads more than once, `--n-hap 4` indicated the ploidy and `--hom-cov` is the homozyous peak in assembly.

| Group | non-contained HiFi reads           |
|-------|------------------------------------|
| LG1_1 | m64053_200110_120759/100206539/ccs |
| LG1_1 | m64053_200110_120759/100270139/ccs |
| LG1_1 | m64053_200110_120759/100272825/ccs |
| LG1_1 | m64053_200110_120759/100402742/ccs |
| LG1_1 | m64053_200110_120759/100467929/ccs |
| LG1_1 | m64053_200110_120759/100468612/ccs |
| LG1_1 | m64053_200110_120759/100534820/ccs |

### Step7 HiC scaffolding and remove artifact

`Juicer` pipeline 

### Annotation
Please follow the https://github.com/baozg/assembly-annotation-pipeline for repeat annotation and gene prediction.


## Contact

Zhigui Bao (zhigui.bao@gmail.com)

