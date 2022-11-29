#!/usr/bin/perl -w
#================================================
#
#         Author: baozhigui
#          Email: zhigui.bao@gmail.com
#         Create: 2021-07-28 20:35:43
#    Description: -
#
#================================================
use strict;
die "\nusage:perl $0 <scores> <reject.list> <ploidy>\n\n"unless (@ARGV==3);
my ($s,$r,$p)=@ARGV;

my %hash;
open I,"$r" or die $!;
while(<I>)
{
    chomp;
    if (/rejected/)
    {
        my $t = (split /\t/,$_)[0];
        $hash{$t}=1;
    }
}
close I;

my %out;
open I,"$s" or die $!;
while(<I>)
{
    chomp;
    next if (/^marker/);
    my ($id,$name,$mg,$mgp);
    if ($p == 4)
    {
        ($id,$name,$mg,$mgp)=(split /\t/,$_)[0,1,9,10];
    }elsif ($p == 2){
        ($id,$name,$mg,$mgp)=(split /\t/,$_)[0,1,7,8];
    }
    next if (exists $hash{$id});
    #if ($mgp < 0.95)
    #{
    #    $mg="NA";
    #}
    push @{$out{$name}},$mg;
}
close I;

foreach my $key (sort keys %out)
{
    my $line = join "\t",@{$out{$key}};
    print "$key\t$line\n";
}
