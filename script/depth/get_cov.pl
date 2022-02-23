#!/usr/bin/perl -w
#================================================
#
#         Author: baozhigui
#          Email: zhigui.bao@gmail.com
#         Create: 2021-06-22 16:35:44
#    Description: -
#
#================================================
use strict;
die "\nusage:perl $0 <sample> <bed> <sum>\n\n"unless (@ARGV==3);
my ($s,$bed,$sum)=@ARGV;

my $mean= `grep -P "total\t" $sum|cut -f4`;
chomp $mean;

open I,"zcat $bed|" or die $!;
while(<I>)
{
    chomp;
    my ($utg,$start,$end,$depth)=(split /\t/,$_);
    my $nd = $depth/$mean;
    print "$utg\_$start\_$end\t$depth\t$nd\n";
}
close I;
