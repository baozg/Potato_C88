import pandas as pd


SAMPLE=pd.read_table("samples.tsv").set_index("samples", drop=False)



rule all:
    input:
        fa = "01.assembly/C88"
        readnum = expand("02.readnum/{sample}.readnum",sample=SAMPLE.index)


rule hifiasm_step1:
    input:
        hifi="data/{sp}.HiFi.fa.gz"
    output:
        utg="01.asm/{sp}.p_utg.fa",
        fa="01.asm/{sp}.p_utg.fa"
    threads: 64
    shell:
        """
        hifiasm -t {threads} -o 01.asm/{wildcards.sp} -l 0 --primary {input.hifi}
        gfatools gfa2fa {output.gfa} > {output.utg}
        """

rule hifi_mapping:
    input:
        fa="01.asm/{sp}.p_utg.fa"
    output:
        bam="02.utg_mapping/{sp}.hifi.sorted.bam",
        bed="02.utg_mapping/{sp}_50kb.regions.bed.gz"
    threads:64
    shell:
        """
        minimap2 -ax map-hifi {input.fa} {input.hifi} -t 64|samtools view -@ 64 -Sb -|samtools sort -o {output.bam} -@ 32 -
        samtools index -@ 32 {output.bam}
        mosdepth -t 64 -b 50000 -Q 1 -F 3840 {wildcards.sp}_50kb {output.bam}
        perl script/class_utg.pl {output.bed} 30 > {output.}
        """
rule depth:
    input:
        bam="01.bam/{sample}.bam"
    output:
        bed="02.depth/01.mosdepth/{sample}.regions.bed.gz",
        sumtxt="02.depth/01.mosdepth/{sample}.mosdepth.summary.txt"
    threads: 20
    params:
        window=50000,
        mq=1,
        flag=3840
    shell:
        """
        /public10/home/sci0009/miniconda3/envs/mosdepth/bin/mosdepth -t {threads} -b {params.windown} -Q {params.mq} -F {params.flag} 02.depth/01.mosdepth/{wildcards.sample} {input.bam}
        """

rule bwa:
    input:
        gz1 = "data/{sample}_1.clean.fq.gz",
        gz2 = "data/{sample}_2.clean.fq.gz"
    output:
        bam = "01.bam/{sample}.bam"
    threads: 8
    shell:
        """
        bwa mem -M -R "@RG\\tID:{wildcards.sample}\\tSM:{wildcards.sample}\\tPL:ILLUMINA" -t {threads} ref/C88.fa {input.gz1} {input.gz2}|samtools view -@ {threads} -Sb - | samtools sort -@ {threads} -o {output.bam} -
        """

rule filter:
    input:
        bam="01.bam/{sample}.bam"
    output:
        readnum="02.readnum/{sample}.readnum"
    threads: 1
    shell:
        """
        samtools view -q 1 -F 3840 {input.bam}|python ../code/04.Genetic_grouping/02_reads_num_window.py ref/C88_50kb.windows.id {output.readnum} 1
        """

rule getCov:
    input:
        bed=rules.depth.output.bed,
        sumtxt=rules.depth.output.sumtxt
    output:
        depth="02.depth/02.normalized_depth/{sample}.depth"
    threads: 1
    params:
        wdir="/public10/home/sci0009/projects/Potato/C88/05.phasing/00.Linkage/p_utg"
    shell:
        """
        perl script/depth/get_cov.pl {wildcards.sample} {params.wdir}/{input.bed} {params.wdir}/{input.sumtxt} > {output.depth}
        """

rule classification_utg:
    input:
    output:
    
rule haplotig_genotype:
    input:
        readnum = expand("02.readnum/{sample}.readnum",sample=SAMPLE.index)
    output:
        readnum = "03.genotype/{name}.readnum",
        score = "03.genotype/{name}.score"
    threads: 64
    params:
        missing=0.8
    shell:
        """
        {python} script/03_contig_filter.py {output.readnum} {params.missing} > 03.genotype/{wildcards.name}.readnum.flt.matrix 
        Rscript script/04_peaks_x_y_hist_win.R 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.peaks_xy.txt
        python script/05_contig_yes_or_no.py 03.genotype/{wildcards.name}.peaks_xy.txt 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.012_score 03.genotype/{wildcards.name}.012.yesno
        awk  -F '\t' '/no/ {for (i=2;i<=NF;i++) printf $i"\t"; printf "\n"}' 03.genotype/{wildcards.name}.012.yesno > 03.genotype/{wildcards.name}.012_failed.yesno
        python script/06_segregation_distortion_marker_yes_or_no.py 03.genotype/{wildcards.name}.012_failed.yesno 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.01.score 03.genotype/{wildcards.name}.01.yesno
        cat 03.genotype/{wildcards.name}.012.score 03.genotype/{wildcards.name}.01.score > {output.score}
        """ 

rule diplotig_genotype:
    input:
        readnum = expand("02.readnum/{sample}.readnum",sample=SAMPLE.index)
    output:
        readnum = "03.genotype/{name}.readnum",
        score = "03.genotype/{name}.score"
    threads: 64
    params:
        missing=0.8
    shell:
        """
        {python} script/03_contig_filter.py {output.readnum} {params.missing} > 03.genotype/{wildcards.name}.readnum.flt.matrix 
        Rscript script/04_peaks_x_y_hist_win.R 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.peaks_xy.txt
        python script/05_contig_yes_or_no.py 03.genotype/{wildcards.name}.peaks_xy.txt 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.012_score 03.genotype/{wildcards.name}.012.yesno
        awk  -F '\t' '/no/ {for (i=2;i<=NF;i++) printf $i"\t"; printf "\n"}' 03.genotype/{wildcards.name}.012.yesno > 03.genotype/{wildcards.name}.012_failed.yesno
        python script/06_segregation_distortion_marker_yes_or_no.py 03.genotype/{wildcards.name}.012_failed.yesno 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.01.score 03.genotype/{wildcards.name}.01.yesno
        cat 03.genotype/{wildcards.name}.012.score 03.genotype/{wildcards.name}.01.score > {output.score}
        """ 

rule triplotig_genotype:
    input:
        readnum = expand("02.readnum/{sample}.readnum",sample=SAMPLE.index)
    output:
        readnum = "03.genotype/{name}.readnum",
        score = "03.genotype/{name}.score"
    threads: 64
    params:
        missing=0.8
    shell:
        """
        {python} script/03_contig_filter.py {output.readnum} {params.missing} > 03.genotype/{wildcards.name}.readnum.flt.matrix 
        Rscript script/04_peaks_x_y_hist_win.R 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.peaks_xy.txt
        python script/05_contig_yes_or_no.py 03.genotype/{wildcards.name}.peaks_xy.txt 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.012_score 03.genotype/{wildcards.name}.012.yesno
        awk  -F '\t' '/no/ {for (i=2;i<=NF;i++) printf $i"\t"; printf "\n"}' 03.genotype/{wildcards.name}.012.yesno > 03.genotype/{wildcards.name}.012_failed.yesno
        python script/06_segregation_distortion_marker_yes_or_no.py 03.genotype/{wildcards.name}.012_failed.yesno 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.01.score 03.genotype/{wildcards.name}.01.yesno
        cat 03.genotype/{wildcards.name}.012.score 03.genotype/{wildcards.name}.01.score > {output.score}
        """

rule refine_group: 
    input:
        readnum = expand("02.readnum/{sample}.readnum",sample=SAMPLE.index)
    output:
        readnum = "03.genotype/{name}.readnum",
        score = "03.genotype/{name}.score"
    threads: 64
    params:
        missing=0.8
    shell:
        """
        {python} script/03_contig_filter.py {output.readnum} {params.missing} > 03.genotype/{wildcards.name}.readnum.flt.matrix 
        Rscript script/04_peaks_x_y_hist_win.R 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.peaks_xy.txt
        python script/05_contig_yes_or_no.py 03.genotype/{wildcards.name}.peaks_xy.txt 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.012_score 03.genotype/{wildcards.name}.012.yesno
        awk  -F '\t' '/no/ {for (i=2;i<=NF;i++) printf $i"\t"; printf "\n"}' 03.genotype/{wildcards.name}.012.yesno > 03.genotype/{wildcards.name}.012_failed.yesno
        python script/06_segregation_distortion_marker_yes_or_no.py 03.genotype/{wildcards.name}.012_failed.yesno 03.genotype/{wildcards.name}.readnum.flt.matrix 03.genotype/{wildcards.name}.01.score 03.genotype/{wildcards.name}.01.yesno
        cat 03.genotype/{wildcards.name}.012.score 03.genotype/{wildcards.name}.01.score > {output.score}
        """

rule group_gfa:
    input:
    output:
    threads:


rule hifiasm_graph_binning:
    input:
        "reads.list"
    output:

