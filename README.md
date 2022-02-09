# Autotetraploid potato: Cooperation-88 🥔

By leveraging the state-of-the-art sequencing technologies and polyploid graph binning, we achieved a chromosome-scale, haplotype-resolved genome assembly of a cultivated potato, Cooperation-88 (C88).

[TOC]


## Pipeline overview
- Hifiasm preliminary assembly
- Classification of utg
- Haplotype-aware genetic phasing
- Polyploidy graph binning of hifiasm
- HiC scaffolding and remove artifact

## Running

Using the snakemake for whole pipeline from preliminary assembly and HiC scaffolding

```bash
snakemake -s Snakefile --cores 64
```

## Step by step


### Step1 Hifiasm preliminary assembly

### Step2 Remapping HiFi reads to utg for classification 

### Step3 Mapping S1 population reads to utg

### Step4 Haplotype-aware Genetic Mapping

### Step5 Utg phasing to reads

### Step6 Polyploidy graph binning of hifiasm

### Step7 HiC scaffolding and remove artifact
