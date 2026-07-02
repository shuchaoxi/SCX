#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use open ':std', ':encoding(UTF-8)';

my $dir = "F:/scx/papers";
my @files = (
    "scx_environment/env_gauge.tex", "scx_industry/main.tex",
    "scx_medicine/med_gauge.tex", "scx_art/art_gauge.tex",
    "scx_distillation_hallucination/main.tex", "scx_audit_economics/audit_economics.tex",
    "scx_hamiltonian_audit/main.tex", "scx_compactness/main.tex",
    "scx_company_valuation/company_valuation.tex", "scx_capstone/auditability_principle.tex",
    "scx_business/business_gauge.tex", "scx_galois_falsifiability/main.tex",
    "scx_information_theory/main.tex", "scx_dev_log/main.tex",
    "scx_acad_mdta_ilh/main.tex", "scx_lambda/lambda_gauge.tex",
    "scx_meta_audit/meta_audit.tex", "scx_civilization/civ_gauge.tex",
    "scx_agentic_audit/main.tex", "scx_hamiltonian/scx_hamiltonian.tex",
    "scx_galois/main.tex", "scx_maintainer_analysis/maintainer_analysis.tex",
    "scx_causal_consensus/main.tex", "scx_instanton/audit_instanton.tex",
    "scx_collective_intelligence/main.tex", "scx_goodhart/goodhart_gauge.tex",
    "scx_geopolitics/main.tex", "scx_education/main.tex",
    "scx_grand_unification/grand_unification.tex", "scx_matrix_theory/main.tex",
    "scx_ip_note/main.tex", "scx_medicine/main.tex", "scx_ml_audit/main.tex",
    "scx_education/edu_gauge.tex", "scx_community/main.tex",
    "scx_astronomy/main.tex", "scx_blockchain/main.tex",
    "scx_governance/main.tex", "scx_elections/main.tex",
    "scx_llm/llm_todo.tex", "scx_business_architecture/main.tex",
    "scx_hardware/checklist.tex", "scx_hardware/ultimate.tex",
    "scx_clean_room/main.tex", "scx_hardware/spec.tex",
    "scx_law/main.tex", "scx_journalism/main.tex",
    "scx_climate/main.tex", "scx_ml_history/main.tex",
    "scx_claude_meta/main.tex", "scx_audit_sword/main.tex",
    "scx_cfd/main.tex", "scx_genomics/main.tex",
    "meta/SCX_MANIFESTO.tex", "meta/SCX_HISTORY.tex",
    "meta/SCX_HISTORY_v2.tex", "egp_merging/main.tex",
);

# First pass: fix \newtheorem patterns  
foreach my $relpath (@files) {
    my $fpath = "$dir/$relpath";
    next unless -f $fpath;
    
    open my $fh, '<:encoding(UTF-8)', $fpath or next;
    my $content = do { local $/; <$fh> };
    close $fh;
    
    my $changed = 0;
    
    # Fix theorem names in \newtheorem
    $content =~ s/\\newtheorem\{([^}]*)\}\{定理\}/\\newtheorem\{$1\}\{Theorem\}/g;
    $content =~ s/\\newtheorem\{([^}]*)\}\{引理\}/\\newtheorem\{$1\}\{Lemma\}/g;
    $content =~ s/\\newtheorem\{([^}]*)\}\{推论\}/\\newtheorem\{$1\}\{Corollary\}/g;
    $content =~ s/\\newtheorem\{([^}]*)\}\{定义\}/\\newtheorem\{$1\}\{Definition\}/g;
    $content =~ s/\\newtheorem\{([^}]*)\}\{注记\}/\\newtheorem\{$1\}\{Remark\}/g;
    $content =~ s/\\newtheorem\{([^}]*)\}\{证明\}/\\newtheorem\{$1\}\{Proof\}/g;
    $content =~ s/\\newtheorem\{([^}]*)\}\{命题\}/\\newtheorem\{$1\}\{Proposition\}/g;
    $content =~ s/\\newtheorem\{([^}]*)\}\{例子\}/\\newtheorem\{$1\}\{Example\}/g;
    $content =~ s/\\newtheorem\{([^}]*)\}\{假设\}/\\newtheorem\{$1\}\{Assumption\}/g;
    
    # Fix \begin{定理} and \end{定理} patterns
    $content =~ s/\\begin\{定理\}/\\begin\{Theorem\}/g;
    $content =~ s/\\end\{定理\}/\\end\{Theorem\}/g;
    $content =~ s/\\begin\{引理\}/\\begin\{Lemma\}/g;
    $content =~ s/\\end\{引理\}/\\end\{Lemma\}/g;
    $content =~ s/\\begin\{推论\}/\\begin\{Corollary\}/g;
    $content =~ s/\\end\{推论\}/\\end\{Corollary\}/g;
    $content =~ s/\\begin\{定义\}/\\begin\{Definition\}/g;
    $content =~ s/\\end\{定义\}/\\end\{Definition\}/g;
    $content =~ s/\\begin\{注记\}/\\begin\{Remark\}/g;
    $content =~ s/\\end\{注记\}/\\end\{Remark\}/g;
    $content =~ s/\\begin\{证明\}/\\begin\{Proof\}/g;
    $content =~ s/\\end\{证明\}/\\end\{Proof\}/g;
    $content =~ s/\\begin\{命题\}/\\begin\{Proposition\}/g;
    $content =~ s/\\end\{命题\}/\\end\{Proposition\}/g;
    $content =~ s/\\begin\{例子\}/\\begin\{Example\}/g;
    $content =~ s/\\end\{例子\}/\\end\{Example\}/g;
    $content =~ s/\\begin\{假设\}/\\begin\{Assumption\}/g;
    $content =~ s/\\end\{假设\}/\\end\{Assumption\}/g;
    
    # Fix standalone theorem references like "定理~\\ref" or "定理\\ref"  
    $content =~ s/定理\s*~?\s*\\ref/Theorem~\\ref/g;
    $content =~ s/引理\s*~?\s*\\ref/Lemma~\\ref/g;
    $content =~ s/推论\s*~?\s*\\ref/Corollary~\\ref/g;
    $content =~ s/定义\s*~?\s*\\ref/Definition~\\ref/g;
    $content =~ s/注记\s*~?\s*\\ref/Remark~\\ref/g;
    $content =~ s/命题\s*~?\s*\\ref/Proposition~\\ref/g;
    
    # Fix section headings with Chinese
    $content =~ s/\\section\{([^}]*定理[^}]*)\}/\\section\{$1\}/g;  # keep as-is, just marker
    
    # Handle specific big block translations
    # "定理" in running text → "Theorem"
    $content =~ s/([^.])定理\b/$1Theorem/g;
    
    if ($content ne (do { open my $f2, '<:encoding(UTF-8)', $fpath; local $/; <$f2> })) {
        open my $out, '>:encoding(UTF-8)', $fpath or die "Cannot write $fpath: $!";
        print $out $content;
        close $out;
        print "FIXED: $relpath\n";
    } else {
        # Still write if we detected changes (avoid false negatives from file read)
        my $before = do { open my $f2, '<:encoding(UTF-8)', $fpath; local $/; <$f2> };
        # Actually let me use a simpler approach
    }
}

print "Theorem names pass complete.\n";

# Now handle the MANIFESTO specifically
my $man = "$dir/meta/SCX_MANIFESTO.tex";
if (-f $man) {
    open my $fh, '<:encoding(UTF-8)', $man or die;
    my $c = do { local $/; <$fh> };
    close $fh;
    $c =~ s/老实人定理/The Honest Person Theorem/g;
    open my $out, '>:encoding(UTF-8)', $man;
    print $out $c;
    close $out;
    print "FIXED: meta/SCX_MANIFESTO.tex\n";
}
