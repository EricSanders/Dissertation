#!/usr/bin/perl


$rootdir = "/RAID/spex3/Tweets/Politiek/Verkiezingen2012";
#$tweetsfile = "$rootdir/PartyCounts/partytweets_20120901-20120911.txt";
$tweetsfile = "$rootdir/PartyCounts/partytweets_20120912-20120912.txt";
$targetdir = "$rootdir/PartyTweets";

open(FILE,$tweetsfile);
@lines = <FILE>;
close(FILE);

foreach $line (@lines) {
    $line =~ s/[\r\n\s]+$//g;
    ($day,$party,$tweet) = split(/\t/,$line,3);
    $month = substr($day,0,6);
    $targetmonthdir = "$targetdir/$month";
    system("mkdir -p $targetmonthdir") unless -e $targetmonthdir;
    if ($fileopen != $day) {
	if ($fileopen) {
	    close(FILE);
	}
	open(FILE,">>$targetmonthdir/${day}:01.out");
	$fileopen = $day;
    }
    if (!$seen{$tweet}) {
	print FILE "$tweet\n";
	$seen{$tweet}++;
    }
}
if ($fileopen) {
    close(FILE);
}
