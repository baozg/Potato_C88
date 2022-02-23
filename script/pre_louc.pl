# !/usr/bin/perl
open(IF,$ARGV[0])||die "Cant open the genotype file.\n";
open(OUT,">".$ARGV[1]);
<IF>;
%hash=();$nloc=0;$nind=0;
while(<IF>)
{
	chomp;
	@sp=split(/\t/,$_);
	$nind=@sp-1;
	$nloc++ if($_ ne "");
	for($i=1;$i<@sp;$i++)
	{
#		if($sp[$i]==0)
#		{
#			$hash{$sp[0]}.='a';
#		}
#		else
#		{
#			$hash{$sp[0]}.='b';
#		}
		if($sp[$i] eq '' || $sp[$i] eq " ")
		{
			print "data were absent\t",$sp[0],"\t",$i,"\n";
		}
		$hash{$sp[0]}.=$sp[$i];
		if($i%5==0)
		{
			$hash{$sp[0]}.=' ';
		}
	}
}
print OUT "name = ".$ARGV[2],"\n";
print OUT "popt = ",$ARGV[3],"\n";
print OUT "nloc = ",$nloc,"\n";
print OUT "nind = ",$nind,"\n";
foreach (keys %hash)
{
	#@pp=split(/\|/,$_);
	#print OUT $pp[0],"|",$pp[1],"\n";
	print OUT $_,"\n";
	for($k=0;$k<length($hash{$_});$k+=60)
	{
		$str=substr($hash{$_},$k,60);
		$str=~s/\s$//;
		print OUT "  ",$str,"\n";
	}
}
close(IF);close(OUT);
