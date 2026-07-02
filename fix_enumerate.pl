#!/usr/bin/perl
use strict;
use warnings;

for my $file ('papers/scx_consciousness/main.tex', 'papers/scx_instanton_k2/main.tex', 'papers/scx_kappa_suppression/main.tex') {
    open(my $fh, '<:utf8', $file) or die "$file: $!";
    my @lines = <$fh>;
    close($fh);
    
    my @out;
    my $i = 0;
    
    while ($i < @lines) {
        my $line = $lines[$i];
        
        # Find enumerate blocks
        if ($line =~ /^\\begin\{enumerate\}/) {
            my $j = $i + 1;
            my $depth = 1;
            my $has_item = 0;
            my $has_content_besides_whitespace = 0;
            
            # Scan the block
            my $k = $i + 1;
            while ($k < @lines && $depth > 0) {
                if ($lines[$k] =~ /^\\begin\{enumerate\}/) { $depth++; }
                if ($lines[$k] =~ /^\\end\{enumerate\}/) { $depth--; last if $depth == 0; }
                if ($lines[$k] =~ /\\item/) { $has_item = 1; }
                if ($lines[$k] =~ /\S/ && $lines[$k] !~ /^\s*$/) { $has_content_besides_whitespace = 1; }
                $k++;
            }
            
            my $block_end = $k;  # line with \end{enumerate}
            
            if (!$has_item && $has_content_besides_whitespace) {
                # Has content but no \item - wrap content in \item
                # For simplicity, add \item before first non-empty line
                my $first_content = $i + 1;
                while ($first_content < $block_end && $lines[$first_content] =~ /^\s*$/) { $first_content++; }
                if ($first_content < $block_end) {
                    # Insert \item
                    push @out, $line;
                    for (my $m = $i + 1; $m < $first_content; $m++) {
                        push @out, $lines[$m];
                    }
                    push @out, "    \\item\n";
                    for (my $m = $first_content; $m <= $block_end; $m++) {
                        push @out, $lines[$m];
                    }
                    $i = $block_end + 1;
                    next;
                }
            }
            
            if (!$has_item) {
                # Empty enumerate - remove the whole block
                $i = $block_end + 1;
                # Also remove preceding \noindent or blank lines
                while (@out > 0 && $out[-1] =~ /^(\s*|\\noindent\s*)$/) {
                    pop @out;
                }
                next;
            }
        }
        
        push @out, $line;
        $i++;
    }
    
    open(my $out_fh, '>:utf8', $file) or die "$file: $!";
    print $out_fh @out;
    close($out_fh);
    print "Fixed $file\n";
}
print "Done!\n";
