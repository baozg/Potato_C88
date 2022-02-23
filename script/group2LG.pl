#!/usr/bin/perl -w
#================================================
#
#         Author: baozhigui
#          Email: zhigui.bao@gmail.com
#         Create: 2021-05-27 22:37:04
#    Description: -
#
#================================================
use strict;
die "\nusage:perl $0 <data.call.gz> <map.txt>\n\n"unless (@ARGV==2);
my ($data,$map)=@ARGV;

my $count;
my %hash;
open I,"$data" or die $!;
while(<I>)
{
    chomp;
    next if (/#|CHR/);
    $count+=1;
    my ($utg) = (split /\t/,$_)[0];
    $hash{$count}="$utg";
}
close I;

print "LG\tMarker\tLOD\n";
$count=0;
open I,"$map" or die $!;
while(<I>)
{
    chomp;
    next if (/^#/);
    next if (/^0/);
    $count+=1;
    print "LG$_\t$hash{$count}\t15\n";
}
close I;
