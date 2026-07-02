#!/usr/bin/perl -CSD
use strict;
use warnings;

# Conservative approach: only remove Chinese-only lines, preserve everything else
my @lines = <>;
my @result;

for my $line (@lines) {
    my $stripped = $line;
    $stripped =~ s/^\s+//;
    $stripped =~ s/\s+$//;
    chomp($stripped);
    
    # NEVER skip lines that contain these LaTeX commands
    if ($stripped =~ /\\(?:documentclass|usepackage|begin|end|newcommand|renewcommand|newtheorem|theoremstyle|maketitle|title|author|date|bibliography|cite|label|ref|input|include)/) {
        push @result, $line;
        next;
    }
    
    # Entity definitions (like \R, \C, \N, \F, \G, etc.) - always keep
    if ($stripped =~ /^\\newcommand\{\\(?:[A-Za-z]|\\[a-zA-Z]+)\}/) {
        push @result, $line;
        next;
    }

    # Skip Chinese-only \section{} and \subsection{} (English equivalent follows)
    if ($stripped =~ /^\\(?:sub)*section\{/) {
        my $cn = () = $stripped =~ /[\x{4e00}-\x{9fff}]/g;
        if ($cn > 0) {
            next; # Skip Chinese section, English follows
        }
    }
    
    # Skip Chinese body text (lines with Chinese but without any LaTeX command)
    # These are Chinese paragraphs that have English equivalents following
    if ($stripped =~ /[\x{4e00}-\x{9fff}]/ && $stripped !~ /^[\\%]/) {
        my $cn = () = $stripped =~ /[\x{4e00}-\x{9fff}]/g;
        my $en = () = $stripped =~ /[a-zA-Z]/g;
        # If mostly Chinese and not inside an environment, skip it
        if ($cn > $en * 2 && $stripped !~ /\\begin|\\end|\\cite|\\ref|\\label|\\textbf|\\textit|\\texttt/) {
            next;
        }
    }
    
    # For mixed lines (LaTeX commands with Chinese), strip Chinese chars
    if ($line =~ /[\x{4e00}-\x{9fff}]/) {
        # Keep the line but strip Chinese from within LaTeX command args only
        # (don't strip from body text - we already skipped those above)
        $line =~ s/[\x{4e00}-\x{9fff}\x{3000}-\x{303f}\x{ff00}-\x{ffef}\x{2018}\x{2019}\x{201c}\x{201d}]+//g;
    }
    
    push @result, $line;
}

# Clean up empty section/subsection
for my $line (@result) {
    next if $line =~ /^\s*\\section\{\s*\}?\s*$/;
    next if $line =~ /^\s*\\subsection\{\s*\}?\s*$/;
    next if $line =~ /^\s*\\textbf\{\s*\}\s*$/;
    print $line;
}
