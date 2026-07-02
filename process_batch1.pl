#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use Encode;

# Process a LaTeX file: remove Chinese text, keep English
# Bilingual pattern: Chinese block followed by English block

sub process_file {
    my ($filepath) = @_;
    
    open(my $fh, '<:utf8', $filepath) or die "Cannot open $filepath: $!";
    my @lines = <$fh>;
    close($fh);
    
    my @out;
    my $skip_chinese = 0;
    
    for (my $i = 0; $i < @lines; $i++) {
        my $line = $lines[$i];
        
        # Remove ctex package
        if ($line =~ /\\usepackage\[UTF8\]\{ctex\}/) {
            next;
        }
        
        # Fix author
        if ($line =~ /\\author\{\}/) {
            push @out, "\\author{SCX}\n";
            next;
        }
        if ($line =~ /\\author\{SCX.*架构师\}/) {
            push @out, "\\author{SCX}\n";
            next;
        }
        if ($line =~ /\\author\{\\SCX\\ Theory Group\}/) {
            push @out, "\\author{SCX}\n";
            next;
        }
        
        # Fix date with Chinese
        if ($line =~ /2026年/) {
            push @out, "\\date{July 2026}\n";
            next;
        }
        
        # Handle bilingual section headings: "中文 / English" -> "English"
        if ($line =~ /^(\\section\{)(.+)(\})/ || $line =~ /^(\\subsection\{)(.+)(\})/) {
            my $cmd = $1;
            my $title = $2;
            my $close = $3;
            if ($title =~ /\// && $title =~ /[\x{4e00}-\x{9fff}]/) {
                # Bilingual: extract English part (without Chinese chars)
                my @parts = split(/\//, $title);
                foreach my $p (@parts) {
                    $p =~ s/^\s+|\s+$//g;
                    if ($p !~ /[\x{4e00}-\x{9fff}]/) {
                        push @out, "$cmd$p$close\n";
                        last;
                    }
                }
                next;
            } elsif ($title =~ /^[\x{4e00}-\x{9fff}\s]+$/ && $title !~ /[a-zA-Z]/) {
                # Pure Chinese heading - skip (English version should be next)
                # Check if next line is English version
                my $j = $i + 1;
                while ($j < @lines && $lines[$j] =~ /^\s*$/) { $j++; }
                if ($j < @lines && $lines[$j] =~ /^(\\section\{)(.+)(\})/ || $lines[$j] =~ /^(\\subsection\{)(.+)(\})/) {
                    # Next line is English heading, keep it
                    # Skip this Chinese heading
                    next;
                }
                # No English version found - keep original
                push @out, $line;
                next;
            }
        }
        
        # Check for Chinese paragraph start markers
        my $stripped = $line;
        $stripped =~ s/^\s+|\s+$//g;
        
        if ($stripped =~ /^\\textbf\{中文\.?\}/ || $stripped eq '\textbf{中文}') {
            # Skip Chinese paragraph - find English version
            my $j = $i + 1;
            while ($j < @lines) {
                my $lj = $lines[$j];
                $lj =~ s/^\s+|\s+$//g;
                if ($lj =~ /^\\textbf\{English\.?\}/ || $lj eq '\textbf{English}') {
                    $i = $j;  # Will add English line on next iteration
                    last;
                }
                if ($lj =~ /^\\end\{abstract\}/ || $lj =~ /^\\vspace/ || $lj =~ /^\\section\{/ || $lj =~ /^\\subsection\{/ || $lj =~ /^\\begin\{/) {
                    $i = $j - 1;
                    last;
                }
                $j++;
            }
            next;
        }
        
        # Check for Chinese title in \title{} - extract English
        if ($line =~ /\\title\{/) {
            # Multi-line title handling - read until matching }
            my $title_block = $line;
            my $depth = 1;
            my $j = $i;
            while ($depth > 0 && $j < @lines) {
                $depth += ($lines[$j] =~ tr/{//) - ($lines[$j] =~ tr/}//);
                $j++;
            }
            my @title_lines = @lines[$i..$j-1];
            my $full_title = join('', @title_lines);
            
            if ($full_title =~ /[\x{4e00}-\x{9fff}]/) {
                # Has Chinese - reconstruct English-only title
                my @eng_lines;
                foreach my $tl (@title_lines) {
                    my $clean = $tl;
                    # Remove Chinese characters from line
                    $clean =~ s/[\x{4e00}-\x{9fff}]+//g;
                    # Remove leading Chinese punctuation
                    $clean =~ s/[\x{3000}-\x{303f}\x{ff00}-\x{ffef}]+//g;
                    # Fix patterns like: \textbf{ 中文部分}  -> \textbf{}
                    $clean =~ s/\\textbf\{[^}]*[\x{4e00}-\x{9fff}][^}]*\}/\\textbf{}/g;
                    # Clean up empty \textbf{} 
                    $clean =~ s/\\textbf\{\}//g;
                    push @eng_lines, $clean;
                }
                push @out, @eng_lines;
                $i = $j - 1;
                next;
            }
        }
        
        # Skip Chinese-only comment lines
        if ($line =~ /^\s*%/ && $line =~ /[\x{4e00}-\x{9fff}]/) {
            my $clean = $line;
            $clean =~ s/[\x{4e00}-\x{9fff}\x{3000}-\x{303f}\x{ff00}-\x{ffef}]//g;
            $clean =~ s/\s*%\s*$/%/;
            if ($clean =~ /^\s*%\s*$/) {
                next;  # All-Chinese comment, drop entirely
            }
            push @out, $clean;
            next;
        }
        
        # Skip Chinese-only lines in body (standalone Chinese lines without English)
        if ($line =~ /[\x{4e00}-\x{9fff}]/ && $line !~ /[a-zA-Z]/ && $line !~ /^\\/) {
            # Pure Chinese line without LaTeX commands - check if it's part of a bilingual block
            next;
        }
        
        # For lines with mixed Chinese+English (not section headings, not titles)
        if ($line =~ /[\x{4e00}-\x{9fff}]/ && $line =~ /[a-zA-Z]/) {
            # Check for bilingual comment or inline text
            if ($line =~ /^\s*%/) {
                my $clean = $line;
                $clean =~ s/[\x{4e00}-\x{9fff}\x{3000}-\x{303f}\x{ff00}-\x{ffef}]//g;
                $clean =~ s/\s*—\s*/ -- /g;
                $clean =~ s/：/:/g;
                if ($clean =~ /^\s*%\s*$/) { next; }
                push @out, $clean;
                next;
            }
        }
        
        push @out, $line;
    }
    
    # Write back
    open(my $out_fh, '>:utf8', $filepath) or die "Cannot write $filepath: $!";
    print $out_fh @out;
    close($out_fh);
}

# Process all three files
my @files = (
    'papers/scx_consciousness/main.tex',
    'papers/scx_instanton_k2/main.tex',
    'papers/scx_kappa_suppression/main.tex',
);

foreach my $f (@files) {
    print "Processing $f...\n";
    process_file($f);
    # Count remaining Chinese
    open(my $fh, '<:utf8', $f) or die;
    my $content = do { local $/; <$fh> };
    close($fh);
    my $count = () = $content =~ /[\x{4e00}-\x{9fff}]/g;
    print "  Remaining Chinese chars: $count\n";
}

print "Done!\n";
