# Autotetraploid potato: Cooperation-88 🥔

By leveraging the state-of-the-art sequencing technologies and polyploid graph binning, we achieved a chromosome-scale, haplotype-resolved genome assembly of a cultivated potato, Cooperation-88 (C88).


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


### Hifiasm preliminary assembly
```bash
hifiasm --
```
### Step2 Remapping HiFi reads to utg for classification
Based on the coverage of 50kb window, divided the window into five utg type (haplotigs,diplotigs,triplotigs,tetraplotigs and repeat region).
```bash
minimap2 -ax map-hifi
samtools index -@ 12 
mosdepth 
```
### Step3 Mapping S1 population reads to utg
```bash
bwa
```


### Step4 Haplotype-aware Genetic Mapping
Since HiC phasing cannot work in the collapsed region, we use genetic grouping for phasing like the diploid potato.

```bash

```

### Step5 Utg phasing to reads
hifiasm gfa keep the non-contained reads record for each utg, we linked the utg phasing to the reads phasing to reduce the mapping bias.
```bash

```

### Step6 Polyploidy graph binning of hifiasm
[hifiasm-dev](https://github.com/chhylp123/hifiasm/tree/hifiasm_dev_debug) have devlopmented polypoidy graph binning. It utlized the non-contained reads information during the assembly graph build process. It can correct the phasing error and extend the phase block with overlap information. So you will have a more contiguous assembly than binning reads. It should work on more than tetraploid and HiC phasing information (ex. AllHiC pipeline)

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
