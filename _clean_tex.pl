#!/usr/bin/perl -CSD
use strict;
use warnings;
binmode(STDOUT, ':utf8');

# Pass 1: Delete Chinese-only body text lines
# These are lines that are mostly Chinese with minimal/no English and no LaTeX commands
my @lines = <>;
my @result;

for my $line (@lines) {
    my $stripped = $line;
    $stripped =~ s/^\s+//;
    chomp($stripped);
    
    # Skip empty lines
    if ($stripped eq '') {
        push @result, $line;
        next;
    }
    
    # Count Chinese and English characters
    my $cn = () = $line =~ /[\x{4e00}-\x{9fff}]/g;
    my $en = () = $line =~ /[a-zA-Z]/g;
    
    # Skip Chinese-only \section{} and \subsection{} (English follows)
    if ($stripped =~ /^\\(?:sub)*section\{/ && $cn > 0 && $en < 20) {
        next;
    }
    
    # Skip Chinese-only body text (no LaTeX command start, mostly Chinese)
    if ($stripped !~ /^[\\%]/ && $cn > 0 && $cn > $en * 3) {
        next;
    }
    
    # Skip the "中文摘要：" line
    if ($stripped =~ /^\\textbf\{中文摘要/) {
        next;
    }
    
    push @result, $line;
}

# Pass 2: Strip remaining Chinese characters from mixed lines
my @final;
for my $line (@result) {
    $line =~ s/[\x{4e00}-\x{9fff}\x{3000}-\x{303f}\x{ff00}-\x{ffef}\x{2018}\x{2019}\x{201c}\x{201d}]+//g;
    push @final, $line;
}

# Pass 3: Remove empty section/subsection commands
for my $line (@final) {
    next if $line =~ /^\s*\\section\{\s*\}\s*$/;
    next if $line =~ /^\s*\\subsection\{\s*\}\s*$/;
    next if $line =~ /^\s*\\textbf\{\s*\}\s*$/;
    print $line;
}
