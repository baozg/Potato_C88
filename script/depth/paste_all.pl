#!/usr/bin/perl -w
#================================================
#
#         Author: baozhigui
#          Email: zhigui.bao@gmail.com
#         Create: 2021-06-23 16:01:57
#    Description: -
#
#================================================
use strict;
die "\nusage:perl $0 <coverage> <ID.txt> <indir>\n\n"unless (@ARGV==3);
my ($cov,$id,$indir)=@ARGV;

my %hash;
open I,"$cov" or die $!;
while(<I>)
{
    chomp;
    my ($w,$t)=(split /\t/,$_)[0,5];
    @{$hash{$w}}=($t);
}
close I;



open I,"$id" or die $!;
while(<I>)
{
    chomp;
    next if (/^samples/);
    open I1,"$indir/$_.depth" or die $!;
    while(<I1>)
    {
        chomp;
        my ($win,$nr)=(split /\t/)[0,2];
        push @{$hash{$win}},$nr;
    }
    close I1;
}
close I;

foreach my $key (keys %hash)
{
    #chomp $hash{$key};
    my @tmp = @{$hash{$key}};
    my $new = join "\t",@tmp[1..$#tmp];
    #$new=~s/\t$//g;
    print "$key\_$tmp[0]\t$new\n";
}
