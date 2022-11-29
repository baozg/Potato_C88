#!/usr/bin/perl -w
#================================================
#
#         Author: baozhigui
#          Email: zhigui.bao@gmail.com
#         Create: 2021-08-09 15:54:35
#    Description: -
#
#================================================
use strict;
die "\nusage:perl $0 <group>\n\n"unless (@ARGV==1);
my ($g)=@ARGV;

my %hash;
open I,"$g" or die $!;
while(<I>)
{
    chomp;
    next if (/^LG\t/);
    my ($lg,$m)=(split /\t/,$_)[0,1];
    my ($utg,$s,$e,$t)=(split /_/,$m)[0,1,2,3];
    if ($t eq "haplotig" or $t eq "repeat")
    {
        $hash{$m}=$lg;
    }else{
        $hash{$utg."_".$s."_".$e."_".$t}.="$lg,";
    }
}
close I;

foreach my $key (sort keys %hash)
{
    my $n = $hash{$key};
    $n=~s/,$//g;
    print "$n\t$key\n";
}
