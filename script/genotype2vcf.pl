#!/usr/bin/perl -w
#================================================
#
#         Author: baozhigui
#          Email: zhigui.bao@gmail.com
#         Create: 2021-05-24 20:30:20
#    Description: -
#
#================================================
use strict;
die "\nusage:perl $0 <geno> <header>\n\n"unless (@ARGV==2);
my ($geno,$header)=@ARGV;

open I,"$header" or die $!;
while(<I>)
{
    chomp;
    print "$_\n";
}
close I;;

#my %hash;
#open I,"$win" or die $!;
#while(<I>)
#{
#    chomp;
#    next if (/^#/);
#    my ($w,$n,$n2)=(split /\t/,$_)[0,1,3];
#    $hash{$w}="$n\t$n2";
#}
#close I;


open I,"$geno" or die $!;
while(<I>)
{
    chomp;
    my @tmp=(split /\t/,$_);
    my $chr=$tmp[0];
    my @geno = @tmp[1..$#tmp];
    for (my $name=0;$name<=$#geno;$name++)
    {
        $geno[$name]=~s#0#0/0#g;
        $geno[$name]=~s#1#0/1#g;
        $geno[$name]=~s#2#1/1#g;
    }
    my $out = join "\t",@geno;
    print "$chr\t1\t.\tA\tT\t999\tPASS\t.\tGT\t0/1\t0/1\t$out\n";

}
close I;


