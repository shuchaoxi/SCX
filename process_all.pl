#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use open ':std', ':encoding(UTF-8)';

my $dir = "F:/scx";
chdir($dir) or die "Cannot chdir to $dir: $!";

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

# Chinese character regex
my $han = qr/[\x{4e00}-\x{9fff}\x{3400}-\x{4dbf}]/;
my $cn_punct = qr/[\x{3000}-\x{303f}\x{ff00}-\x{ffef}\x{2000}-\x{206f}]/;
my $cn_full = qr/[\x{4e00}-\x{9fff}\x{3400}-\x{4dbf}\x{3000}-\x{303f}\x{ff00}-\x{ffef}\x{ff0c}\x{3002}\x{ff01}\x{ff1f}\x{ff1b}\x{ff1a}\x{201c}\x{201d}\x{2018}\x{2019}\x{3010}\x{3011}\x{300a}\x{300b}\x{ff08}\x{ff09}\x{2026}\x{2014}]/;

for my $file (@files) {
    print "=== $file ===\n";
    open(my $fh, '<:encoding(UTF-8)', $file) or do { warn "Cannot open: $!"; next; };
    my $content = do { local $/; <$fh> };
    close($fh);
    
    my $orig = $content;
    
    # ==========================================================
    # STEP 1: Structural LaTeX changes
    # ==========================================================
    
    # ctexart -> article
    $content =~ s/\\documentclass\[.*?\]\{ctexart\}/\\documentclass[12pt,a4paper]{article}/g;
    
    # Remove ctex package (with or without options)
    $content =~ s/\\usepackage\[UTF8\]\{ctex\}\s*\n?//g;
    $content =~ s/\\usepackage\{ctex\}\s*\n?//g;
    
    # Remove xeCJK package
    $content =~ s/\\usepackage\{xeCJK\}\s*\n?//g;
    
    # Remove CJK font settings (various patterns)
    $content =~ s/\\setCJKmainfont\{[^}]*\}(?:\[[^\]]*\])?\s*\n?//g;
    $content =~ s/\\setmainfont\{[^}]*\}\s*\n?//g;
    
    # Remove fontspec if only used for CJK (check if still needed)
    # Keep fontspec for now, some files use it for other fonts
    
    # Fix theorem environment names (Chinese -> English)
    my %theorem_map = (
        '定理' => 'Theorem',
        '引理' => 'Lemma',
        '推论' => 'Corollary',
        '定义' => 'Definition',
        '注记' => 'Remark',
        '猜想' => 'Conjecture',
        '例'   => 'Example',
        '命题' => 'Proposition',
        '假设' => 'Assumption',
        '判据' => 'Criterion',
    );
    
    for my $cn (keys %theorem_map) {
        my $en = $theorem_map{$cn};
        # Pattern: \newtheorem{name}{定理} or \newtheorem{name}[counter]{定理}
        $content =~ s/\{\Q$cn\E\}/{$en}/g;
    }
    
    # \mathsf -> \textsf
    $content =~ s/\\mathsf\b/\\textsf/g;
    
    # \author{...} -> \author{SCX}
    $content =~ s/\\author\{[^}]*\}/\\author{SCX}/g;
    # Handle multi-line \author
    $content =~ s/\\author\{[^}]*\}[^{]*\{[^}]*\}[^{]*\{[^}]*\}/\\author{SCX}/gs;
    
    # ==========================================================
    # STEP 2: Remove/translate Chinese text
    # ==========================================================
    
    # For bilingual text in \textit{}, remove Chinese and keep English
    # Pattern: \textit{Chinese text} on its own (where English already exists nearby)
    $content =~ s/\\textit\{[^}]*$han[^}]*\}//g;
    
    # Remove standalone Chinese comment lines at file headers
    $content =~ s/^%\s*[^\n]*$han[^\n]*\n//gm;
    
    # Remove Chinese-only lines (lines that are mostly Chinese)
    $content =~ s/^[^a-zA-Z0-9\\%\$\\{\\}]*$han[^a-zA-Z0-9\\%\$\\{\}\n]*\n//gm;
    
    # Remove remaining Chinese characters from mixed lines
    $content =~ s/[$cn_full]+//g;
    
    # ==========================================================
    # STEP 3: Cleanup
    # ==========================================================
    
    # Remove lines that became empty or whitespace-only
    $content =~ s/^\s*\n//gm;
    
    # Remove multiple blank lines
    $content =~ s/\n{3,}/\n\n/g;
    
    # Remove trailing whitespace
    $content =~ s/[ \t]+$//gm;
    
    # Fix section headings that became empty
    $content =~ s/\\section\{[\s\/]*\}/\\section{Section}/g;
    $content =~ s/\\subsection\{[\s\/]*\}/\\subsection{Subsection}/g;
    
    # Write back if changed
    if ($content ne $orig) {
        open(my $out, '>:encoding(UTF-8)', $file) or die "Cannot write: $!";
        print $out $content;
        close($out);
        print "  UPDATED\n";
    } else {
        print "  No changes\n";
    }
}

print "\nDone!\n";
