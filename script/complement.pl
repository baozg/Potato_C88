#!/usr/bin/perl -w
#================================================
#
#         Author: baozhigui
#          Email: zhigui.bao@gmail.com
#         Create: 2021-07-29 19:39:20
#    Description: -
#
#================================================
use strict;
die "\nusage:perl $0 <score>\n\n"unless (@ARGV==1);
my ($score)=@ARGV;

open I,"$score" or die $!;
while(<I>)
{
    chomp;
    my @tmp=(split /\t/,$_);
    my @out;
    for (my $i=1;$i<=$#tmp;$i++)
    {
        my $dtmp = 2-$tmp[$i];
        push @out,$dtmp;
    }
    my $line = join "\t",@out;
    print "$tmp[0]\t$line\n";
}
close I;
