author: Qian Zhou  zhouqian_solab@163.com
data: 6/24/2020


This pipeline is used to phase and group the assembled sequences of diploid genome based on the low-coverage sequencing of a segregation population.####
The input files are the assembled genome draft and the Illumina reads of sequenced individuals. The output are the groups presenting the two haplotypes of each chromosome, including a number of scaffolds or contigs.###


###Map the sequenced reads of the segregation population to the assembled scaffolds or contigs and calculated the number of uniquely mapped reads.##
python3.2 01_scaf_2_window.py RH_scaf.fasta.len 400000 ref_window_marker.id

for i in {1..200}; do
        bwa mem -t 5 RH_scaf.fa RH-$i.R1.fq.gz RH-$i.R2.fq.gz | samtools view -bS - > bam_files/RH-$i.bam;
        samtools view bam_files/RH-$i.bam | python3.2 02_reads_num_window.py ref_window_marker.id readnum/RH-$i.readnum 50;
done;


######get the 0/1/2 genotype for every marker and detect completely linked makres###
####the following lines will be performed sequentially
p='RH.200samples'
awk '!/#/ {print $1"\t"$NF}' readnum/RH-1.readnum > $p.readnum
for i in {2..10}; do paste $p.readnum <(awk '!/#/ {print $NF}'  readnum/RH-$i.readnum) > tmp.readnum && mv tmp.readnum $p.readnum; done;
python3.2 ./03_contig_filter.py ../$p.readnum $p.readnum.flt.matrix
Rscript ./04_peaks_x_y_hist_win.R $p.readnum.flt.matrix $p.peaks_xy.txt
python3.2 ./05_contig_yes_or_no.py $p.peaks_xy.txt $p.readnum.flt.matrix  $p.012_score $p.012.yes_no
awk  -F '\t' '/no/ {for (i=2;i<=NF;i++) printf $i"\t"; printf "\n"}'  $p.012.yes_no > 012_failed.yesno
python3.2 ./06_segregation_distortion_marker_yes_or_no.py 012_failed.yesno $p.readnum.flt.matrix  $p.01.score  $p.01.score.yesno
cat $p.012_score  $p.01.score >  $p.score

####remove the redundant markers that with >0.99 score correlation ####
Rscript ./07_correlation.R $p.score  $p.score.correlation.out
python3.2 ./08_mark_strong_linked_marker.py $p.score.correlation.out  score_cor_0.99.marker score_redundant.marker
python3.2 ./09_flt_completely_linked_marker.py  $p.score score_redundant.marker marker_score_rmd

###prepare files for JoinMap and perform genetic grouping using JoinMap###
python3.2 ./marker_4_joinmap.py $p.marker $p.4.joinmap
pre_louc.pl $p.4.joinmap $p.loc RH F2

###extract the groups from the *grpng.txt output by the JoinMap4.0###
python3.2 ./grpng_2_LG.py $p.grpng.txt $p.grpng.out
###each group determined by JoinMap4.0 is split to two sub-groups according to the number of mapped reads.###
###the output sub-groups present the haplotype of diploid genome.
python3.2 ./split_LG.py $p.grpng.out $p.readnum.flt.matrix $p.24LG.out

####calculate the correlation between the grouped markers and the un-grouped markers ####
python3.2 ./10_query_reference_marker_set.py  $p.readnum.flt.matrix $p.grpng.out  target.readnum  query.readnum
Rscript 03_target_query_correlation.R  query.readnum target.readnum readnum.correlation.out
python3.2 ./11_show_strongest_second_correlation.py  query.readnum target.group readnum.correlation.out query.readnum_strongest_cor.xls
awk '$3>=0.7  {if ($4==$7) print $1"\t"$2"\t"$5"\t"$4; else if ($4==$10) print $1"\t"$2"\t"$8"\t"$4; else if ($7==$10) print $1"\t"$5"\t"$8"\t"$7 }' query.readnum_strongest_cor.xls  >good.cor.marker


###combine the $p.24LG.out and the good.cor.marker to generagte the complete haplotype-resolved genetic map.
###determine the groups of assembled contigs and unitigs based on the grouped window markers.

cat <(awk '{print $2"\t"$1}') good.cor.marker >all_win_group
python3.2 ./12_ctg_group.py ref_window_marker.id all_win_group ctg_group_based_on_win
for i in {1..12}; do awk -v lg="chr"$i"_1" '$NF~lg {sum +=$2} END {print lg"\tlength\t"sum} ' ctg_group_based_on_win  >> lg.len; done;
for i in {1..12}; do awk -v lg="chr"$i"_2" '$NF~lg {sum +=$2} END {print lg"\tlength\t"sum} ' ctg_group_based_on_win  >> lg.len; done;
