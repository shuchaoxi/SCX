#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use Encode;

# Cleanup script: fix garbled remnants after Chinese removal
# Removes empty/placeholder text blocks, fixes headings, titles, theorem names

sub is_garbled_line {
    my ($line) = @_;
    my $stripped = $line;
    $stripped =~ s/^\s+|\s+$//g;
    
    # Empty line
    return 0 if $stripped eq '';
    
    # Lines with just \textbf{.} (was \textbf{中文.})
    return 1 if $stripped eq '\textbf{.}';
    
    # Lines that are just LaTeX spacing commands
    return 1 if $stripped =~ /^\\\\\[\d+\.?\d*em\]$/;
    
    # Empty subsection/section
    return 1 if $stripped =~ /^\\(sub)?section\{\}$/;
    
    # Lines with Chinese dashes or bare punctuation that indicate removed Chinese
    if ($stripped =~ /^——/ || $stripped =~ /^[—…、，。；：""''（）【】《》\s]+$/) {
        return 1;
    }
    
    # LaTeX content that begins with just a dangling math symbol/period (Chinese was removed)
    if ($stripped =~ /^\$\w+\$\s*$/ && $stripped !~ /[a-zA-Z]{3,}/) {
        return 1;  
    }
    
    return 0;
}

sub cleanup_file {
    my ($filepath) = @_;
    
    open(my $fh, '<:utf8', $filepath) or die "Cannot open $filepath: $!";
    my @lines = <$fh>;
    close($fh);
    
    my @out;
    my $i = 0;
    
    while ($i < @lines) {
        my $line = $lines[$i];
        my $stripped = $line;
        $stripped =~ s/^\s+|\s+$//g;
        chomp($line);
        
        # Fix: \section{ / Name} -> \section{Name}
        if ($line =~ /^(\\section\{)\s*\/\s*([^}]+)(\})/) {
            push @out, "$1$2$3\n";
            $i++;
            next;
        }
        if ($line =~ /^(\\subsection\{)\s*\/\s*([^}]+)(\})/) {
            push @out, "$1$2$3\n";
            $i++;
            next;
        }
        
        # Fix: empty \section{} followed by English \section{...}
        if ($stripped =~ /^\\section\{\}$/ || $stripped =~ /^\\section\{\s*\/?\s*\}$/) {
            # Look ahead for English section heading
            my $j = $i + 1;
            while ($j < @lines && $lines[$j] =~ /^\s*$/) { $j++; }
            if ($j < @lines && $lines[$j] =~ /^\\section\{([^}]+)\}/) {
                # Next line is English section, skip this empty one
                $i++;
                next;
            }
            # No English version - skip entirely
            $i++;
            next;
        }
        
        # Fix: empty \subsection{} followed by English \subsection{...}
        if ($stripped =~ /^\\subsection\{\}$/ || $stripped =~ /^\\subsection\{\s*\/?\s*\}$/) {
            my $j = $i + 1;
            while ($j < @lines && $lines[$j] =~ /^\s*$/) { $j++; }
            if ($j < @lines && $lines[$j] =~ /^\\subsection\{([^}]+)\}/) {
                $i++;
                next;
            }
            $i++;
            next;
        }
        
        # Fix: garbled \textbf{.} markers and their subsequent garbled content
        if ($stripped eq '\textbf{.}') {
            # This was a Chinese paragraph marker. Skip until next structural element or English marker.
            my $j = $i + 1;
            while ($j < @lines) {
                my $ls = $lines[$j];
                $ls =~ s/^\s+|\s+$//g;
                last if $ls eq '\textbf{English.}' || $ls eq '\textbf{English}';
                last if $ls =~ /^\\textbf\{English\.\}/;
                last if $ls =~ /^\\section\{/ || $ls =~ /^\\subsection\{/;
                last if $ls =~ /^\\begin\{/;
                last if $ls =~ /^\\end\{abstract\}/;
                last if $ls eq '\vspace{0.5em}';
                $j++;
            }
            if ($j < @lines && ($lines[$j] =~ /\\textbf\{English\.?\}/ || $lines[$j] =~ /^\\textbf\{English\}/)) {
                $i = $j;  # Jump to English block
                next;
            }
            $i = $j;
            next;
        }
        
        # Fix: garbled line (just punctuation/symbols from removed Chinese)
        if (is_garbled_line($line)) {
            $i++;
            next;
        }
        
        # Fix: title blocks with garbled remnants 
        # \textbf{$\\kappa$ } should keep the English
        if ($stripped eq '\textbf{$\\kappa$ }') {
            # This was: 抑制悖论 — just skip 
            $i++;
            next;
        }
        
        # Fix: lines like "\\[0.3em]" (title spacing after Chinese removal)
        if ($stripped =~ /^\\\\\[0\.3em\]$/ || $stripped =~ /^\\\\\[0\.5em\]$/) {
            # Check context - if alone between empty lines, skip
            $i++;
            next;
        }
        
        # Skip blocks of garbled lines (consecutive garbled non-English lines)
        if ($stripped ne '' && $stripped !~ /^[\\%]/ && $stripped !~ /[a-zA-Z]{3,}/) {
            # Line has no significant English words - likely garbled Chinese remnant
            # But check if it's part of an English block first
            my $has_math = ($stripped =~ /\$/);
            my $has_punct = ($stripped =~ /^[—…、，。；：""''（）【】《》\s\.\,\(\)\[\]\{\}\-]+$/);
            if (!$has_math && $has_punct) {
                $i++;
                next;
            }
            # If it's very short (< 10 chars) and no English words
            if (length($stripped) < 15 && $stripped !~ /[a-zA-Z]{2,}/ && $stripped !~ /^\\/) {
                $i++;
                next;
            }
        }
        
        # Fix: remove problematic blank lines from section/subsection gaps  
        # (handled by output, just push the line)
        
        push @out, "$line\n";
        $i++;
    }
    
    # Post-processing: remove triple+ blank lines
    my $result = join('', @out);
    $result =~ s/\n\n\n\n+/\n\n\n/g;
    $result =~ s/\n\n\n/\n\n/g;  # Max 1 blank line between paragraphs
    
    # Fix remaining bilingual heading patterns
    $result =~ s/\\section\{\s*\/\s*/\\section\{/g;
    $result =~ s/\\subsection\{\s*\/\s*/\\subsection\{/g;
    
    # Remove empty \textbf{} 
    $result =~ s/\\textbf\{\}//g;
    
    # Fix double section commands (empty section followed by English)
    $result =~ s/\\section\{\}\s*\n\s*\\section\{/\\section\{/g;
    $result =~ s/\\subsection\{\}\s*\n\s*\\subsection\{/\\subsection\{/g;
    
    # Fix title remnants
    $result =~ s/\\textbf\{\$\\kappa\$ \}/\\textbf{\$\\kappa\$ Suppression Paradox}/g;
    
    # Restore spacing around sections
    $result =~ s/\n(\\section\{)/\n\n$1/g;
    $result =~ s/\n(\\subsection\{)/\n\n$1/g;
    $result =~ s/\n\n\n(\\section)/\n\n$1/g;
    $result =~ s/\n\n\n(\\subsection)/\n\n$1/g;
    
    open(my $out_fh, '>:utf8', $filepath) or die "Cannot write $filepath: $!";
    print $out_fh $result;
    close($out_fh);
}

my @files = (
    'papers/scx_consciousness/main.tex',
    'papers/scx_instanton_k2/main.tex',
    'papers/scx_kappa_suppression/main.tex',
);

foreach my $f (@files) {
    print "Cleanup $f...\n";
    cleanup_file($f);
    open(my $fh, '<:utf8', $f) or die;
    my $content = do { local $/; <$fh> };
    close($fh);
    my $count = () = $content =~ /[\x{4e00}-\x{9fff}]/g;
    print "  Remaining Chinese: $count\n";
}

print "Done cleanup!\n";
