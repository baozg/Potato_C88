#!/usr/bin/perl -w
#================================================
#
#         Author: baozhigui
#          Email: zhigui.bao@gmail.com
#         Create: 2021-06-30 16:10:02
#    Description: -
#
#================================================
use strict;
die "\nusage:perl $0 <mat>\n\n"unless (@ARGV==1);
my ($mat)=@ARGV;

print "MarkerName\tSampleName\tratio\n";
open I,"$mat" or die $!;
while(<I>)
{
    chomp;
    my @tmp=(split /\t/,$_);
    my $max=0;
    for (my $i=1;$i<=$#tmp;$i++)
    {
        if ($tmp[$i]>$max)
        {
            $max=$tmp[$i];
        }
    }
    for (my $i=1;$i<=$#tmp;$i++)
    {
        my $ratio=$tmp[$i]/($max+100);
        #my $y = 1000*$ratio;
        #my $x=1000-$y;
        print "$tmp[0]\tS$i\t$ratio\n";
    }
}

close I;
