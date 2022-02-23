#!/usr/bin/perl -w
#================================================
#
#         Author: baozhigui
#          Email: zhigui.bao@gmail.com
#         Create: 2022-02-10 15:16:03
#    Description: -
#
#================================================
use strict;
die "\nusage:perl $0 <region.depth.bed> <haploid peak>\n\n"unless (@ARGV==2);
my ($bed,$p)=@ARGV;
my $sp = $p*1.5;


open I,"zcat $bed|" or die $!;
while(<I>)
{
    chomp;
    my ($chr,$s,$e,$d)=(split /\t/,$_);
    if ($d > 3 and $d <= $sp)
    {
        print "$chr\_$s\_$e\thaplotig\n";
    }elsif ($d > $sp and $d <= $sp+$p)
    {
        print "$chr\_$s\_$e\tdiplotig\n";
    }elsif ($d > $sp+$p and $d <= $sp+$p*2)
    {
        print "$chr\_$s\_$e\ttriplotig\n";
    }elsif ($d > $sp+$p*2 and $d <= $sp+$p*3)
    {
        print "$chr\_$s\_$e\ttetraplotig\n";
    }elsif ($d < 3 or $d > $sp+$p*3)
    {
        print "$chr\_$s\_$e\trepeat\n";
    }
}
close I;


