#!/usr/bin/perl
use strict;
use warnings;

# Find files that HAD physics removed (check if they use braket but don't define it)
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
    open(my $fh, '<:encoding(UTF-8)', $f) or return undef;
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

my $fix_count = 0;
my $total = 0;

foreach my $f (@files) {
    $total++;
    my $c = read_tex($f);
    next unless defined $c;
    my $modified = 0;
    
    # Check if file uses \braket but doesn't define it (and doesn't load braket package)
    if ($c =~ /\\braket/ && $c !~ /\\newcommand\{\\braket\}/ && $c !~ /\\usepackage\{braket\}/) {
        # Add \braket definition after the last \usepackage line or after \documentclass
        my $def = "\\newcommand{\\braket}[1]{\\langle #1 \\rangle}\n";
        if ($c =~ s/(\\usepackage\{[^}]+\}\s*\n)(?!.*\\usepackage)/$1$def/s) {
            $modified = 1;
        } elsif ($c =~ s/(\\documentclass[^\n]*\n)/$1$def/) {
            $modified = 1;
        }
    }
    
    # Check if file uses \ket but doesn't define it
    if ($c =~ /\\ket\{/ && $c !~ /\\newcommand\{\\ket\}/ && $c !~ /\\usepackage\{braket\}/ && $c !~ /\\usepackage\{physics\}/) {
        my $def = "\\newcommand{\\ket}[1]{|#1\\rangle}\n";
        if ($c =~ s/(\\usepackage\{[^}]+\}\s*\n)(?!.*\\usepackage)/$1$def/s) {
            $modified = 1;
        }
    }
    
    # Check if file uses \bra but doesn't define it
    if ($c =~ /\\bra\{/ && $c !~ /\\newcommand\{\\bra\}/ && $c !~ /\\usepackage\{braket\}/ && $c !~ /\\usepackage\{physics\}/) {
        my $def = "\\newcommand{\\bra}[1]{\\langle #1|}\n";
        if ($c =~ s/(\\usepackage\{[^}]+\}\s*\n)(?!.*\\usepackage)/$1$def/s) {
            $modified = 1;
        }
    }
    
    if ($modified) {
        write_tex($f, $c);
        $fix_count++;
        print "  ADDED braket def: $f\n";
    }
}

print "\nTotal: $fix_count files fixed out of $total\n";
