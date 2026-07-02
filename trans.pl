#!/usr/bin/perl -CSD
use strict;
use warnings;
use utf8;

# Process each file
for my $file (@ARGV) {
    open(my $fh, '<:encoding(UTF-8)', $file) or die "Cannot open $file: $!";
    my $content = do { local $/; <$fh> };
    close($fh);
    
    my $original = $content;
    
    # Basic replacements
    $content =~ s/\\mathsf\{SCX\}/\\textsf\{SCX\}/g;
    $content =~ s/ctexart/article/g;
    
    # Remove CJK packages
    $content =~ s/\\usepackage\[UTF8[^\]]*\]\{ctex\}.*\n//g;
    $content =~ s/\\usepackage\{CJKutf8\}.*\n//g;
    $content =~ s/\\usepackage\{xeCJK\}.*\n//g;
    $content =~ s/\\setCJKmainfont\{[^}]*\}.*\n//g;
    $content =~ s/\\setCJKsansfont\{[^}]*\}.*\n//g;
    $content =~ s/\\setCJKmonofont\{[^}]*\}.*\n//g;
    $content =~ s/\\newfontfamily\\cjkfont\{[^}]*\}.*\n//g;
    
    # Theorem names
    my %theorems = (
        '定理' => 'Theorem', '引理' => 'Lemma', '推论' => 'Corollary',
        '定义' => 'Definition', '注记' => 'Remark', '猜想' => 'Conjecture',
        '假设' => 'Assumption', '例' => 'Example', '原理' => 'Principle',
        '注' => 'Note', '证明' => 'Proof',
    );
    for my $cn (keys %theorems) {
        my $en = $theorems{$cn};
        $content =~ s/\{$cn\}/\{$en\}/g;
    }
    
    # Chinese dates
    $content =~ s/(\d{4})年(\d{1,2})月(\d{1,2})日/$1-$2-$3/g;
    $content =~ s/(\d{4})年(\d{1,2})月/$1-$2/g;
    
    # Chinese punctuation
    $content =~ s/：/: /g;
    $content =~ s/。/./g;
    $content =~ s/，/, /g;
    $content =~ s/；/; /g;
    
    # Strip Chinese from section/caption brackets
    $content =~ s/(\\(?:sub)?section\{)([^}]*?)\s+\p{Han}+[^}]*(\})/$1$2$3/g;
    $content =~ s/(\\caption\{)([^}]*?)\s+\p{Han}+[^}]*(\})/$1$2$3/g;
    
    # Remove Chinese abstract/对照 blocks
    $content =~ s/\\noindent\\textbf\{中文Abstract\.\}.*?(?=\\medskip|\\noindent\\textbf\{English)//gs;
    $content =~ s/\\noindent\\textbf\{中文对照：?\}.*?(?=\\medskip|\\noindent)//gs;
    $content =~ s/.*中文对照.*\n//g;
    $content =~ s/.*中文问题陈述.*\n//g;
    $content =~ s/\\subsection\{中文\}.*?(?=\\subsection|\\section)//gs;
    
    # Remove lines that are >40% Chinese characters (excluding LaTeX commands)
    my @lines = split(/\n/, $content);
    my @filtered;
    for my $line (@lines) {
        next if $line =~ /^\s*$/;  # keep empty lines but we'll add them back
        my $stripped = $line;
        $stripped =~ s/[\s\\\{\}\$]//g;
        next if length($stripped) == 0;
        my $chinese = () = $stripped =~ /\p{Han}/g;
        my $total = length($stripped);
        if ($total > 0 && $chinese / $total > 0.4) {
            # Line is >40% Chinese - skip unless it has LaTeX
            if ($line !~ /\\[a-zA-Z]/ && $line !~ /\$/) {
                next;
            }
        }
        push @filtered, $line;
    }
    
    if (@filtered != @lines) {
        $content = join("\n", @filtered);
    }
    
    # Fix author
    $content =~ s/\\author\{[^}]*\p{Han}[^}]*\}/\\author\{SCX\}/g;
    
    # Write back if changed
    if ($content ne $original) {
        open(my $out, '>:encoding(UTF-8)', $file) or die "Cannot write $file: $!";
        print $out $content;
        close($out);
        my $remaining = () = $content =~ /\p{Han}/g;
        print "$remaining Chinese chars remaining: $file\n";
    } else {
        print "No changes: $file\n";
    }
}
