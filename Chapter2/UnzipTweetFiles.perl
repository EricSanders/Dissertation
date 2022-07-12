#!/usr/bin/perl
use File::Basename;

$sourcedir = "/RAID/databases/tweet_etks";
$targetdir = "/RAID/spex3/Tweets/Politiek/Verkiezingen2012/AllTweets";

@months = (201209);
#@days = (20120901 .. 20120911);
@days = (20120912);
foreach $day (@days) {
    $unzipdays{$day}++;
}

foreach $month (@months) {
    open(FIND,"find $sourcedir/$month -name \"*.gz\" -print |");
    @gzfiles = <FIND>;
    close(FIND);
    
    $targetmonthdir = "$targetdir/$month";
    system("mkdir -p $targetmonthdir") unless -e $targetmonthdir;
    
    foreach $gzfile (@gzfiles) {
	chomp $gzfile;
	($gzfilename,$gzfilepath,$gzfilesuffix) = fileparse($gzfile,".gz");
 	$gzday = substr($gzfilename,0,8);
	if ($unzipdays{$gzday}) {
	    $targetgzfile = "$targetmonthdir/$gzfilename";

	    print "gunzip -c $gzfile > $targetgzfile\n";
	    system("gunzip -c $gzfile > $targetgzfile");
	}
    }
}
