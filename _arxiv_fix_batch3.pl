#!/usr/bin/perl
use strict;
use warnings;

my $fix_count = 0;
my $total = 0;

# Collect all .tex files under /f/scx/papers/
my @files;
sub collect {
    my $dir = shift;
    opendir(my $dh, $dir) or return;
    while (my $f = readdir($dh)) {
        next if $f eq '.' || $f eq '..';
        my $path = "$dir/$f";
        if (-d $path) { collect($path); }
        elsif ($f =~ /\.tex$/) { push @files, $path; }
    }
    closedir($dh);
}
collect('/f/scx/papers');
@files = sort @files;

sub read_tex {
    my $f = shift;
    open(my $fh, '<:encoding(UTF-8)', $f) or do { warn "Cannot open $f: $!"; return undef; };
    local $/;
    my $c = <$fh>;
    close $fh;
    return $c;
}

sub write_tex {
    my ($f, $c) = @_;
    open(my $fh, '>:encoding(UTF-8)', $f) or do { warn "Cannot write $f: $!"; return; };
    print $fh $c;
    close $fh;
}

foreach my $f (@files) {
    $total++;
    my $content = read_tex($f);
    next unless defined $content;
    my $modified = 0;

    # Fix 1: Add \pdfoutput=1 before first \documentclass (if not already present)
    if ($content !~ /\\pdfoutput=1/) {
        $content =~ s/(\\documentclass)/\\pdfoutput=1\n$1/;
        $modified = 1;
    }

    # Fix 2: Remove \usepackage[utf8]{inputenc} and \usepackage{inputenc}
    if ($content =~ s/\\usepackage\[utf8\]\{inputenc\}\s*\n?//g) { $modified = 1; }
    if ($content =~ s/\\usepackage\{inputenc\}\s*\n?//g) { $modified = 1; }

    # Fix 3: Remove \usepackage{physics} (with optional options)
    if ($content =~ s/\\usepackage(\[[^\]]*\])?\{physics\}\s*\n?//g) { $modified = 1; }

    # Fix 4: Remove linkcolor=blue
    if ($content =~ s/linkcolor\s*=\s*blue\s*,?\s*//g) { $modified = 1; }
    if ($content =~ s/,\s*linkcolor\s*=\s*blue\s*//g) { $modified = 1; }

    # Fix 5: \documentclass{ctexart} → \documentclass{article}
    if ($content =~ s/\\documentclass\{ctexart\}/\\documentclass\{article\}/g) { $modified = 1; }
    if ($content =~ s/\\documentclass\[([^\]]*)\]\{ctexart\}/\\documentclass[$1]\{article\}/g) { $modified = 1; }
    # Remove CJK-related packages
    if ($content =~ s/\\usepackage(\[[^\]]*\])?\{ctex\}\s*\n?//g) { $modified = 1; }
    if ($content =~ s/\\usepackage(\[[^\]]*\])?\{xeCJK\}\s*\n?//g) { $modified = 1; }
    if ($content =~ s/\\usepackage(\[[^\]]*\])?\{fontspec\}\s*\n?//g) { $modified = 1; }
    if ($content =~ s/\\usepackage(\[[^\]]*\])?\{CJKutf8\}\s*\n?//g) { $modified = 1; }
    if ($content =~ s/\\usepackage(\[[^\]]*\])?\{CJKspace\}\s*\n?//g) { $modified = 1; }
    if ($content =~ s/\\usepackage(\[[^\]]*\])?\{CJK\}\s*\n?//g) { $modified = 1; }

    # Fix 6: \author{...} → \author{SCX} (single-line only)
    if ($content =~ s/\\author\{[^}]*\}/\\author\{SCX\}/g) { $modified = 1; }

    if ($modified) {
        write_tex($f, $content);
        $fix_count++;
        print "  FIXED: $f\n" if $fix_count <= 50 || $fix_count % 10 == 0;
    }
}

print "\nTotal: $fix_count files modified out of $total\n";
