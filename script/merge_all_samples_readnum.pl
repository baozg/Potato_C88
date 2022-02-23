#!/usr/bin/perl -w
#================================================
#
#         Author: baozhigui
#          Email: zhigui.bao@gmail.com
#         Create: 2021-05-20 22:37:21
#    Description: -
#
#================================================
use strict;
use Data::Dumper;
die "\nusage:perl $0 <sample.list> <marker.bed> <window.id> <dir>\n\n"unless (@ARGV==4);
my ($sam,$bed,$id,$dir)=@ARGV;

my %hash;

my $count=1;
open I,"$sam" or die $!;
while(<I>)
{
    chomp;
    next if (/^samples/);
    $hash{$count}=$_;
    $count ++;
}
close I;

#====
my %out;
open I,"$bed" or die $!;
while(<I>)
{
    chomp;
    my ($w,$t)=(split /\t/,$_)[0,1];
    @{$out{$w}}=($t);
}
close I;


my %win;
open I,"$id" or die $!;
while(<I>)
{
    chomp;
    next if (/^#/);
    my ($w,$u,$s,$e)=(split /\t/,$_)[0,1,3,4];
    $s-=1;
    $win{$w}="$u\_$s\_$e";
}
close I;

#====
foreach my $t (sort keys %hash)
{
    my $test = $hash{$t};
    open I,"$dir/$test.readnum" or die $!;
    while(<I>)
    {
        chomp;
        next if (/^#/);
        my ($wid,$num,$norm)=(split /\t/,$_)[0,1,3];
        my $ctg = $win{$wid};
        push @{$out{$ctg}},$norm;
    }
    close I;
}


#====
foreach my $t (sort keys %out)
{
    my @line = @{$out{$t}};
    my $newline = join "\t",@line[1..$#line];
    print "$t\_$line[0]\t$newline\n"
}
