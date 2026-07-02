#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use Encode;

# Final aggressive cleanup
# Remove: empty Chinese-originated blocks, garbled text, fix comments/titles/dates

sub final_cleanup {
    my ($filepath) = @_;
    
    open(my $fh, '<:utf8', $filepath) or die;
    my @lines = <$fh>;
    close($fh);
    
    my @out;
    my $i = 0;
    
    while ($i < @lines) {
        my $line = $lines[$i];
        chomp($line);
        my $s = $line;
        $s =~ s/^\s+|\s+$//g;
        
        # ===== Fix specific known issues =====
        
        # Fix author
        if ($s eq '\author{}' || $s =~ /\\author\{\\SCX\\ Theory Group\}/) {
            push @out, "\\author{SCX}";
            $i++;
            next;
        }
        
        # Fix date with garbled numbers  
        if ($s =~ /^\\date\{2026/) {
            push @out, "\\date{July 2026}";
            $i++;
            next;
        }
        
        # Fix garbled comments (lines starting with % that have Chinese remnants)
        if ($s =~ /^%\s*SCX\s*(C\d*)?\s*[:—]\s*$/) {
            # Garbled comment - skip
            $i++;
            next;
        }
        if ($s =~ /^%\s*SCX\s*[—–-]\s*$/) {
            $i++; next;
        }
        if ($s eq '% Chinese+English' || $s =~ /Chinese\+English/) {
            $i++; next;
        }
        
        # Fix garbled title line: \textbf{Situs2-}
        if ($s =~ /^\\textbf\{Situs/ && $s =~ /-$/ && length($s) < 30) {
            # This was the Chinese title - restore English version
            push @out, "    \\textbf{Higher-Dimensional Audit Instantons: 2-Form Flux on the Situs Complex\\\\and Topological Detection of Circular Inconsistency}\\\\[0.5em]";
            $i++;
            next;
        }
        
        # ===== Skip garbled text blocks =====
        
        # Line with only LaTeX math symbols + Chinese punctuation remnants
        if ($s =~ /^\$\w+\$\s*\$\w+\$\s*——$/ || $s =~ /^\$\w+\$\s*\$\w+\$/) {
            $i++; next;
        }
        
        # Lines that are just: \textbf{.} or \textbf{Something .} (Chinese marker remnants)
        if ($s =~ /^\\textbf\{\.?\}\s*$/ || $s =~ /^\\textbf\{\s*\.\s*\}/) {
            $i++; next;
        }
        if ($s =~ /^\\textbf\{\$\w+\$\s*\.?\}/ || $s =~ /^\\textbf\{[^}]{0,15}\.\}/) {
            # Short \textbf{...} with period - likely Chinese remnant
            my $content = $1 if $s =~ /\\textbf\{([^}]+)\}/;
            if (!$content || length($content) < 15) {
                $i++; next;
            }
        }
        
        # Garbled list items: \item \textbf{.} ... (Chinese text removed)
        if ($s =~ /^\\item\s+\\textbf\{\.?\}/ || $s =~ /^\\item\s+\\textbf\{[^}]{0,20}\.\}/) {
            $i++; next;
        }
        
        # Empty text{} after Chinese removal
        if ($s =~ /\\text\{\}/) {
            $line =~ s/\\text\{\}//g;
            $s = $line;
            $s =~ s/^\s+|\s+$//g;
        }
        
        # Lines like "outliers————``''$\\kappa: \\R \\to [0,1]$$S_i(x)$``''" 
        # These had Chinese removed, leaving just punctuation and LaTeX inline
        if ($s =~ /^[—–-]{2,}/ || $s =~ /^``''/) {
            $i++; next;
        }
        
        # Lines that are mostly just LaTeX math with no English words  
        if ($s =~ /\$/ && $s !~ /[a-zA-Z]{3,}/ && $s !~ /^\\begin/ && $s !~ /^\\end/ && $s !~ /^\\label/ && $s !~ /^\\caption/ && $s !~ /^\\cite/) {
            # Check if it looks like garbled Chinese remnant with math
            if ($s =~ /^\s*\$\w+\s*\(?\w*\)?\s*\$\s*\$\w+\s*\(?\w*\)?\s*\$\s*[—–-]*\s*$/) {
                $i++; next;
            }
            if ($s =~ /^\s*\\\$\S+\\\$\s*\\\$\S+\\\$\s*\\\$\S+\\\$\s*$/) {
                # Multiple math blocks with no English text - likely garbled
                $i++; next;
            }
        }
        
        # Empty noindent followed by nothing useful
        if ($s eq '\noindent') {
            # Check if next line is useful
            my $j = $i + 1;
            while ($j < @lines && $lines[$j] =~ /^\s*$/) { $j++; }
            my $next = $lines[$j] || '';
            $next =~ s/^\s+|\s+$//g;
            if ($next =~ /^\\textbf\{English\.?\}/ || $next =~ /^\\begin\{/ || $next =~ /^\\section\{/) {
                # Useful follows - keep \noindent
                push @out, $line;
                $i++;
                next;
            }
            # Nothing useful follows - skip
            $i++;
            next;
        }
        
        # Fix: \subsection{SCX} which was "与SCX核心框架的关系"
        if ($s eq '\subsection{SCX}') {
            push @out, "\\subsection{Relation to the SCX Core Framework}";
            $i++;
            next;
        }
        
        # Fix: \normalsize \SCX\  · \Cfour\ \\ (garbled title line)  
        if ($s =~ /^\\normalsize\s+\\SCX\s*·\s*\\Cfour/) {
            push @out, "    \\normalsize SCX Equality Framework \\· C4 Extension";
            $i++;
            next;
        }
        
        push @out, $line;
        $i++;
    }
    
    my $result = join("\n", @out) . "\n";
    
    # Post-fixes
    $result =~ s/\\author\{SCX Theory Group\}/\\author{SCX}/g;
    $result =~ s/\\date\{20267\}/\\date{July 2026}/g;
    
    # Remove lines that are just stray " $E$ $\\AuditOp$ ——" type
    $result =~ s/^\s*\$\w+\$\s*\$\w+\$\s*——\s*$//gm;
    
    # Remove triple+ blank lines
    $result =~ s/\n\n\n\n+/\n\n\n/g;
    $result =~ s/\n\n\n/\n\n/g;
    
    # Remove empty \textbf{} 
    $result =~ s/\\textbf\{\}//g;
    
    # Fix double noindents
    $result =~ s/\\noindent\n\n\\noindent/\\noindent/g;
    
    open(my $out_fh, '>:utf8', $filepath) or die;
    print $out_fh $result;
    close($out_fh);
}

my @files = (
    'papers/scx_consciousness/main.tex',
    'papers/scx_instanton_k2/main.tex',
    'papers/scx_kappa_suppression/main.tex',
);

foreach my $f (@files) {
    print "Final cleanup $f...\n";
    final_cleanup($f);
}
print "Done!\n";
