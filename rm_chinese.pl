#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use open ':std', ':encoding(UTF-8)';

# Process all 8 Group D files
my @files = (
    "papers/scx_industry/main.tex",
    "papers/scx_information_theory/main.tex",
    "papers/scx_instanton/audit_instanton.tex",
    "papers/scx_journalism/main.tex",
    "papers/scx_lambda/lambda_gauge.tex",
    "papers/scx_law/main.tex",
    "papers/scx_maintainer_analysis/maintainer_analysis.tex",
    "papers/scx_matrix_theory/main.tex",
);

chdir("F:/scx") or die "Cannot chdir: $!";

for my $file (@files) {
    print "Processing $file...\n";
    open(my $fh, '<:encoding(UTF-8)', $file) or do { warn "Cannot open $file: $!"; next; };
    my @lines = <$fh>;
    close($fh);
    
    my $changed = 0;
    my @new_lines;
    for my $line (@lines) {
        my $orig = $line;
        
        # Skip pure math/LaTeX command lines
        if ($line =~ /^\s*(\\|%|\$|\{|\}|\[|\])/) {
            push @new_lines, $line;
            next;
        }
        
        # Only process lines with Chinese
        if ($line =~ /\p{Han}/) {
            # Strategy: Remove Chinese text segments, keep English/LaTeX
            
            # Remove \textit{Chinese text} blocks (keep if English inside)
            $line =~ s/\\textit\{([^}]*[\x{4e00}-\x{9fff}][^}]*)\}//g;
            
            # Remove standalone Chinese sentences (between periods)
            $line =~ s/[\x{4e00}-\x{9fff}\x{3000}-\x{303f}\x{ff00}-\x{ffef}，。！？；：""''【】《》（）…—]+//g;
            
            # Clean up resulting whitespace
            $line =~ s/\s{2,}/ /g;
            $line =~ s/^\s+//;
            $line =~ s/\s+$//;
            
            # If line is now empty or just whitespace+punct, skip it
            if ($line =~ /^\s*$/) {
                $changed = 1;
                next;
            }
            # If it's just a period or other punctuation, skip
            if ($line =~ /^\s*[.。\/]\s*$/) {
                $changed = 1;
                next;
            }
            # If it became just " / " or similar, skip
            if ($line =~ /^\s*\/\s*$/) {
                $changed = 1;
                next;
            }
        }
        
        if ($orig ne $line) {
            $changed = 1;
        }
        push @new_lines, $line . "\n";
    }
    
    if ($changed) {
        open(my $out, '>:encoding(UTF-8)', $file) or die "Cannot write $file: $!";
        print $out @new_lines;
        close($out);
        print "  Written: $file\n";
    } else {
        print "  No changes: $file\n";
    }
}

print "All done!\n";
