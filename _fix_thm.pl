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

foreach my $relpath (@files) {
    my $fpath = "$dir/$relpath";
    next unless -f $fpath;
    
    open my $fh, '<:encoding(UTF-8)', $fpath or next;
    my $c = do { local $/; <$fh> };
    close $fh;
    
    my $orig = $c;
    
    # Fix \newtheorem patterns - use different approach to avoid shell expansion
    $c =~ s/\\newtheorem\{([^}]*)\}\{定理\}/\\newtheorem{$1}{Theorem}/g;
    $c =~ s/\\newtheorem\{([^}]*)\}\{引理\}/\\newtheorem{$1}{Lemma}/g;
    $c =~ s/\\newtheorem\{([^}]*)\}\{推论\}/\\newtheorem{$1}{Corollary}/g;
    $c =~ s/\\newtheorem\{([^}]*)\}\{定义\}/\\newtheorem{$1}{Definition}/g;
    $c =~ s/\\newtheorem\{([^}]*)\}\{注记\}/\\newtheorem{$1}{Remark}/g;
    $c =~ s/\\newtheorem\{([^}]*)\}\{证明\}/\\newtheorem{$1}{Proof}/g;
    $c =~ s/\\newtheorem\{([^}]*)\}\{命题\}/\\newtheorem{$1}{Proposition}/g;
    $c =~ s/\\newtheorem\{([^}]*)\}\{例子\}/\\newtheorem{$1}{Example}/g;
    $c =~ s/\\newtheorem\{([^}]*)\}\{假设\}/\\newtheorem{$1}{Assumption}/g;
    
    # Fix \begin/\end
    foreach my $pair (['定理','Theorem'], ['引理','Lemma'], ['推论','Corollary'],
                       ['定义','Definition'], ['注记','Remark'], ['证明','Proof'],
                       ['命题','Proposition'], ['例子','Example'], ['假设','Assumption']) {
        my ($cn, $en) = @$pair;
        $c =~ s/\\begin\{$cn\}/\\begin\{$en\}/g;
        $c =~ s/\\end\{$cn\}/\\end\{$en\}/g;
    }
    
    if ($c ne $orig) {
        open my $out, '>:encoding(UTF-8)', $fpath or die "Cannot write $fpath: $!";
        print $out $c;
        close $out;
        print "FIXED: $relpath\n";
    }
}

# Handle MANIFESTO
my $man = "$dir/meta/SCX_MANIFESTO.tex";
if (-f $man) {
    open my $fh, '<:encoding(UTF-8)', $man or die;
    my $c = do { local $/; <$fh> };
    close $fh;
    $c =~ s/老实人/The Honest Person/g;
    open my $out, '>:encoding(UTF-8)', $man;
    print $out $c;
    close $out;
    print "FIXED: meta/SCX_MANIFESTO.tex\n";
}

print "DONE.\n";
