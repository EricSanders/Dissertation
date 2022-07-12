#!/usr/bin/perl
use File::Basename;

#$tweetset = 'AllTweets';
$tweetset = 'PartyTweets';

$rootdir = "/RAID/spex3/Tweets/Politiek/Verkiezingen2012";
$sourcedir = "$rootdir/$tweetset";
$targetdir = "$rootdir/PartyCounts";
$pollfile = "/RAID/t0/people/sanders/Twitter/Politiek/Verkiezingen2012/allepeilingen_com_20120101-20130113.tsv";

@days = (20120907 .. 20120912);
#@days = (20120902 .. 20120911);
#@days = (20120901);
#@days = (20120912);
foreach $day (@days) {
    $alldays{$day}++;
}

&readnrrealvotes;
&readpolls($pollfile);
#exit(0);

open(WORDS,">$targetdir/partywords_$days[0]-$days[$#days].txt") || die "Cannot open words file";
open(TWEETS,">$targetdir/partytweets_$days[0]-$days[$#days].txt") || die "Cannot open tweets file";

$parties{"vvd"} = ["vvd"]; #volkspartij=33 (0.024% (33/140000))
$parties{"pvda"} = ["pvda","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+arbeid"]; #partij van de arbeid=148 (0.106%)
$parties{"sp"} = ["sp"]; #socialistische partij=46 (0.033%)
$parties{"pvv"} = ["pvv","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+vrijheid"]; #partij voor de vrijheid<=49, partij van de vrijheid<=22
$parties{"cda"} = ["cda"]; #democratisch appel=5
$parties{"d66"} = ["d\'?66"]; #d'66=263 (0.188%), d-66=4, democraten( ')66 <=42
$parties{"gl"} = ["gl","groen.?links"]; #groen links=586 (0.188%), groen-links=22
$parties{"cu"} = ["cu","christen.?unie"]; #christen unie=131, christen-unie=4
$parties{"pvdd"} = ["pvdd","partij\\s+v(oor\\s+|an\\s+|.)?d(e|.)?\\s+dieren"]; #dierenpartij=72
$parties{"sgp"} = ["sgp"]; #staatkundig=15
$parties{"50plus"} = ["50[^\\d]?(\\+|plus)"]; #vijftig( )plus<=27, vijftig+<=3 


print STDERR "Start reading twitter files\n";
foreach $day (@days) {
    $month = substr($day,0,6);
    $sourcemonthdir = "$sourcedir/$month";
    open(FIND,"find $sourcemonthdir -name \"$day*.out\" -print |");
    @outfiles = <FIND>;
    close(FIND);
    
    foreach $outfile (@outfiles) {
	chomp $outfile;
	($outfilename,$outfilepath,$outfilesuffix) = fileparse($outfile,".out");
 	$outday = substr($outfilename,0,8);

	print STDERR "  Reading $outfile...";
	open(OUTFILE,$outfile);
	@lines = <OUTFILE>;
	close(OUTFILE);
	
	foreach $line (@lines) {
	    $line =~ s/[\r\n\s]+$//g;
	    foreach $party (keys %parties) {
		#print "looking at $party\n";
		foreach $partypattern (@{$parties{$party}}) {
		    #print "looking at $partypattern\n";
		    if ($line =~ /(\s|\.|,|;|:|!|\?|\@|\#|^)($partypattern)(\s|\.|,|;|:|!|\?|$)/i) {
			$daypartycounts{$day}{$party}++;
			$daypartycounts{"all"}{$party}++;
			$daypartycounts{$day}{"all"}++;
			$daypartycounts{"all"}{"all"}++;
			print WORDS "$day\t$2\n";
			$partyfound++;
		    }
		}
		if ($partyfound) {
		    print TWEETS "$day\t$party\t$line\n";
		    $partyfound=0;
		}
	    }
	}
	print STDERR "done!\n";
    }
}
print STDERR "Done reading twitter files\n";

close(WORDS);
close(TWEETS);



open(RES,">$targetdir/partyresults_$days[0]-$days[$#days].txt") || die "Cannot open results file";
print RES "Twitter mentions\n--------\n";
foreach $day (@days) {
    print RES "$day\n--------\n";
    print RES "\t\t\t";
    foreach $pollinst (sort keys %{$pollvotes{$day}{'vvd'}}) {
	print RES "\t$pollinst";
    }
    print RES "\n";
    foreach $party (sort {$nrrealvotes{$b} <=> $nrrealvotes{$a} } keys %nrrealvotes) {
	print RES "$party\t";
	$perc = sprintf("%.2f",100*$daypartycounts{$day}{$party}/$daypartycounts{$day}{"all"});
	print RES "$perc\t($daypartycounts{$day}{$party} / $daypartycounts{$day}{all})";
	foreach $pollinst (sort keys %{$pollvotes{$day}{'vvd'}}) {
	    if ($pollvotes{$day}{$party}{$pollinst}) {
		$perc = sprintf("%.2f",100*$pollvotes{$day}{$party}{$pollinst}/150);
		$sum += $pollvotes{$day}{$party}{$pollinst};
		$nrinst++;
		print RES "\t$perc";
	    }
	    else {
		print RES "\t-";
	    }
	}
	print RES "\n";
    }
    print RES "--------\n";
}
print RES "All days\n--------\n";
foreach $party (sort {$nrrealvotes{$b} <=> $nrrealvotes{$a} } keys %nrrealvotes) {
    print RES "$party\t";
    $perc = sprintf("%.2f",100*$daypartycounts{"all"}{$party}/$daypartycounts{"all"}{"all"});
    $percrealvotes{$party} = sprintf("%.2f",100 * $nrrealvotes{$party} / $totnrvotes);
    print RES "$perc ($daypartycounts{all}{$party} / $daypartycounts{all}{all})\t$percrealvotes{$party} ($nrrealvotes{$party} / $totnrvotes)\n";
}
close(RES);

open(RRES,">$targetdir/partyresults_r_$days[0]-$days[$#days].txt") || die "Cannot open results file";
print RRES "daybe";
foreach $party (sort {$nrrealvotes{$b} <=> $nrrealvotes{$a} } keys %nrrealvotes) {
    print RRES "\t${party}Tweets\t${party}Poll";
}
print RRES "\n";
foreach $day (@days) {
    print RRES &nrdaysbeforeelection($day);
    foreach $party (sort {$nrrealvotes{$b} <=> $nrrealvotes{$a} } keys %nrrealvotes) {
	$perc = sprintf("%.1f",100*$daypartycounts{$day}{$party}/$daypartycounts{$day}{"all"});
	print RRES "\t$perc";
	if ($pollvotes{$day}{$party}{"Average"}) {
	    $perc = sprintf("%.1f",100*$pollvotes{$day}{$party}{"Average"}/150);
	}
	else {
	    $perc = "NaN";
	}
	print RRES "\t$perc";
    }
    print RRES "\n";
}
close(RRES);


open(RALLRES,">$targetdir/partyresults_r_all_$days[0]-$days[$#days].txt") || die "Cannot open results file";
print RALLRES "daybe";
foreach $party (sort {$nrrealvotes{$b} <=> $nrrealvotes{$a} } keys %nrrealvotes) {
    print RALLRES "\t${party}Tweets\t${party}Election";
}
print RALLRES "\n";
print RALLRES "all";
foreach $party (sort {$nrrealvotes{$b} <=> $nrrealvotes{$a} } keys %nrrealvotes) {
    $perc = sprintf("%.1f",100*$daypartycounts{"all"}{$party}/$daypartycounts{"all"}{"all"});
    $percrealvotes{$party} = sprintf("%.1f",100 * $nrrealvotes{$party} / $totnrvotes);
    print RALLRES "\t$perc\t$percrealvotes{$party}";
}
print RALLRES "\n";

close(RALLRES);


sub readnrrealvotes {
    $nrrealvotes{"vvd"} = 2504948;
    $nrrealvotes{"pvda"} = 2340750;
    $nrrealvotes{"pvv"} = 950263;
    $nrrealvotes{"cda"} = 801620;
    $nrrealvotes{"sp"} = 909853;
    $nrrealvotes{"d66"} = 757091;
    $nrrealvotes{"gl"} = 219896;
    $nrrealvotes{"cu"} = 294586;
    $nrrealvotes{"sgp"} = 196780;
    $nrrealvotes{"pvdd"} = 182162;
#    $nrrealvotes{"piratenpartij"} = 30600;
#    $nrrealvotes{"mens"} = 18310;
#    $nrrealvotes{"nederlandlokaal"} = 2842;
#    $nrrealvotes{"libertarischpartij"} = 4163;
#    $nrrealvotes{"dpk"} = 7363;
    $nrrealvotes{"50plus"} = 177631;
#    $nrrealvotes{"libdem"} = 2126;
#    $nrrealvotes{"antieuropapartij"} = 2013;
#    $nrrealvotes{"sopn"} = 12982;
#    $nrrealvotes{"pvdtoekomst"} = 8194;
#    $nrrealvotes{"nxd"} = 62;

    foreach $party (keys %nrrealvotes) {
	$totnrvotes += $nrrealvotes{$party};
    }

#    print RES "Election results:\n\n";
#    foreach $party (sort {$nrrealvotes{$b} <=> $nrrealvotes{$a} } keys %nrrealvotes) {
#	$percrealvotes{$party} = sprintf("%.2f",100 * $nrrealvotes{$party} / $totnrvotes);
#	print RES "$party\t\t$percrealvotes{$party} ($nrrealvotes{$party} / $totnrvotes)\n";
#    }
#    print RES "-----\n\n";

}

sub readpolls {
    ($pollsfilename) = @_;
    open(FILE,$pollsfilename);
    @lines = <FILE>;
    close(FILE);

    foreach $line (@lines) {
	$line =~ s/[\r\n\s]+$//g;
	($pollday,$polparty,$pollinst,$pollvotes) = split(/\t/,$line);
	$lcpolparty = lc $polparty;
	$lcpolparty = 'gl' if $polparty eq 'GroenLinks';
	$lcpolparty = 'cu' if $polparty eq 'ChristenUnie';
#	print "$pollday,$polparty,$pollinst,$pollvotes\n";
	($myday = $pollday) =~ s/\-//g;
	next unless $alldays{$myday};
	$pollvotes{$myday}{$lcpolparty}{$pollinst} = $pollvotes;
#	print "$pollday,$polparty,$pollinst,$pollvotes\n";
    }

    foreach $day (@days) {
#	print "$day\n";
	foreach $pollinst (sort keys %{$pollvotes{$day}{'vvd'}}) {
#	    print "\t$pollinst";
	}
#	print "\tAverage\n";
	foreach $party (sort {$nrrealvotes{$b} <=> $nrrealvotes{$a} } keys %nrrealvotes) {
#	    print "$party";
	    foreach $pollinst (sort keys %{$pollvotes{$day}{$party}}) {
		$perc = sprintf("%.2f",100*$pollvotes{$day}{$party}{$pollinst}/150);
		$sum += $pollvotes{$day}{$party}{$pollinst};
		$nrinst++;
#		print "\t$perc";
	    }
	    if ($nrinst > 0) {
		$averageperc = sprintf("%.2f",100*($sum/$nrinst)/150);
		$pollvotes{$day}{$party}{'Average'} = $sum/$nrinst;
#		print "\t$averageperc";
		$sum = 0;
		$nrinst = 0;
	    }
#	    print "\n";
	}
#	print "- - -\n";
    }
}

sub nrdaysbeforeelection {
    ($day) = @_;
    return 20120912 - $day; #works only for 1-11 September 2012
}

			
