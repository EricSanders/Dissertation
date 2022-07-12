#!/usr/bin/perl
use File::Basename;

$sourcedir = "/RAID/spex3/Tweets/Politiek/Verkiezingen2012";
$targetdir = "$sourcedir/WordCounts";

@months = (201209);
@days = (20120901 .. 20120911);
#@days = (20120901);
foreach $day (@days) {
    $countdays{$day}++;
}

$sourcemonthdir = "$sourcedir/$month";

print STDERR "Start reading twitter files\n";
foreach $month (@months) {
    open(FIND,"find $sourcemonthdir -name \"*.out\" -print |");
    @outfiles = <FIND>;
    close(FIND);
    
    foreach $outfile (@outfiles) {
	chomp $outfile;
	($outfilename,$outfilepath,$outfilesuffix) = fileparse($outfile,".out");
 	$outday = substr($outfilename,0,8);
	if ($countdays{$outday}) {
	    print STDERR "  Reading $outfile...";
	    open(OUTFILE,$outfile);
	    @lines = <OUTFILE>;
	    close(OUTFILE);
	    
	    foreach $line (@lines) {
		$line =~ s/[\r\n\s]+$//g;
		@words = split(/\s+/,$line);
		foreach $wordnr (1 .. $#words) {
		    $word = $words[$wordnr];
		    $countwords{$outday}{$word}++;
		    $countwords{"all"}{$word}++;
#		    print "$word\n";
		}
	    }
	    print STDERR "done\n";
	}
    }
}
print STDERR "Reading twitter files done\n";
print STDERR "\n";
print STDERR "Start writing wordcount files\n";

foreach $day (sort keys %countwords) {
    print STDERR "  Writing wordcounts of $day...";
    $targetfile = "$targetdir/$day.txt";
    open(WCFILE,">$targetfile");
    foreach $word (sort { $countwords{$day}{$b} <=> $countwords{$day}{$a} } keys %{$countwords{$day}}) {
#    foreach $word (sort %{$countwords{$day}}) {
	print WCFILE $word."\t".$countwords{$day}{$word}."\n";
    }
    close(WCFILE);
    print STDERR "done\n";
   
}
print STDERR "done\n";
