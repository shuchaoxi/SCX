#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use Encode;

# Batch 2: Supplementary .tex files excluded by batch1.sh (64 files)
my @FILES = (
    "papers/supplementary/corrections/viewpoint1_correction.tex",
    "papers/supplementary/corrections/viewpoint4_correction.tex",
    "papers/supplementary/corrections/viewpoint5_correction.tex",
    "papers/supplementary/history/codex_reviews/01_SCX_核心框架_数学分析.tex",
    "papers/supplementary/history/codex_reviews/02_SCX_子模块_详细设计.tex",
    "papers/supplementary/history/codex_reviews/03_竞争分析_数据估值与主动学习.tex",
    "papers/supplementary/history/codex_reviews/04_竞争分析_MoE与蒸馏.tex",
    "papers/supplementary/history/codex_reviews/05_数学根源与证明.tex",
    "papers/supplementary/history/codex_reviews/06_实现架构与实验设计.tex",
    "papers/supplementary/history/codex_reviews/07_two_layer_descriptors_error_driven_state_discovery.tex",
    "papers/supplementary/history/codex_reviews/08_distillation_de_virus_math_roots_and_multi_scenario.tex",
    "papers/supplementary/history/codex_reviews/paper_framework_review_report_five_reviewers_synthesis.tex",
    "papers/supplementary/history/explorations/a2_adversarial_verification.tex",
    "papers/supplementary/history/explorations/a2_correlation_analysis.tex",
    "papers/supplementary/history/explorations/a2_rigorous_analysis.tex",
    "papers/supplementary/history/explorations/asymptotic_theory.tex",
    "papers/supplementary/history/explorations/bbp_spectral_proxy.tex",
    "papers/supplementary/history/explorations/cluster_consistency_proof.tex",
    "papers/supplementary/history/explorations/cluster_consistency_v2.tex",
    "papers/supplementary/history/explorations/cluster_consistency_v3.tex",
    "papers/supplementary/history/explorations/deep_math_connections.tex",
    "papers/supplementary/history/explorations/exact_constant_minimax.tex",
    "papers/supplementary/history/explorations/feature_strength_via_stability.tex",
    "papers/supplementary/history/explorations/final_math_verification.tex",
    "papers/supplementary/history/explorations/lemma_AB_bahadur_rao_f1.tex",
    "papers/supplementary/history/explorations/lemma_CD_chernoff_adaptive.tex",
    "papers/supplementary/history/explorations/lemma_EF_lowerbound_aggregation.tex",
    "papers/supplementary/history/explorations/minimax_lower_bound_proof.tex",
    "papers/supplementary/history/explorations/minimax_lower_bound_v2.tex",
    "papers/supplementary/history/explorations/minimax_optimality.tex",
    "papers/supplementary/history/explorations/random_matrix_connection.tex",
    "papers/supplementary/history/explorations/review_bbp_spectral_proxy.tex",
    "papers/supplementary/history/explorations/review_cluster_consistency.tex",
    "papers/supplementary/history/explorations/review_minimax_lower_bound.tex",
    "papers/supplementary/history/explorations/review_minimax_v2.tex",
    "papers/supplementary/history/explorations/scx_galois_deep.tex",
    "papers/supplementary/history/explorations/verification_exact_constant.tex",
    "papers/supplementary/history/self_evolution/01_symbol_system.tex",
    "papers/supplementary/history/self_evolution/02_dynamical_system.tex",
    "papers/supplementary/history/self_evolution/03_online_learning_regret.tex",
    "papers/supplementary/history/self_evolution/04_bayesian_update.tex",
    "papers/supplementary/history/self_evolution/05_stochastic_approximation.tex",
    "papers/supplementary/history/self_evolution/06_fixed_point_convergence.tex",
    "papers/supplementary/history/self_evolution/07_completeness.tex",
    "papers/supplementary/history/self_evolution/08_theory_connections.tex",
    "papers/supplementary/history/self_evolution/09_verification_report.tex",
    "papers/supplementary/history/self_evolution/10_lyapunov_analysis.tex",
    "papers/supplementary/history/self_evolution/11_convergence_rate.tex",
    "papers/supplementary/history/self_evolution/12_edge_cases.tex",
    "papers/supplementary/history/self_evolution/CERCIS_NAMING.tex",
    "papers/supplementary/history/self_evolution/final_review_jmlr.tex",
    "papers/supplementary/history/self_evolution/final_review_nature.tex",
    "papers/supplementary/history/self_evolution/hostile_review.tex",
    "papers/supplementary/history/self_evolution/MATHEMATICAL_GENEALOGY.tex",
    "papers/supplementary/history/self_evolution/multi_head_spring_and_positional_encoding_analysis.tex",
    "papers/supplementary/history/self_evolution/ppe_rigorous_derivation.tex",
    "papers/supplementary/history/self_evolution/README.tex",
    "papers/supplementary/history/self_evolution/situs_final_verification.tex",
    "papers/supplementary/history/self_evolution/situs_physical_validation.tex",
    "papers/supplementary/history/self_evolution/spring_convergence_analysis.tex",
    "papers/supplementary/history/self_evolution/spring_hostile_review.tex",
    "papers/supplementary/history/self_evolution/SPRING_NAMING.tex",
    "papers/supplementary/history/theory/PROOF_CHAIN_AUDIT.tex",
    "papers/supplementary/history/theory/scx_8theorems_review.tex",
);

# Physics package command replacements
sub replace_physics_cmds {
    my ($content) = @_;
    $content =~ s/\\dv\s*\{([^}]+)\}\s*\{([^}]+)\}/\\frac{d $1}{d $2}/g;
    $content =~ s/\\dv\*\s*\{([^}]+)\}\s*\{([^}]+)\}/\\frac{d $1}{d $2}/g;
    $content =~ s/\\pdv\s*\{([^}]+)\}\s*\{([^}]+)\}/\\frac{\\partial $1}{\\partial $2}/g;
    $content =~ s/\\pdv\*\s*\{([^}]+)\}\s*\{([^}]+)\}/\\frac{\\partial $1}{\\partial $2}/g;
    $content =~ s/\\abs\s*\{([^}]+)\}/\\left|$1\\right|/g;
    $content =~ s/\\norm\s*\{([^}]+)\}/\\left\\|$1\\right\\|/g;
    $content =~ s/\\ket\s*\{([^}]+)\}/|$1\\rangle/g;
    $content =~ s/\\bra\s*\{([^}]+)\}/\\langle $1|/g;
    $content =~ s/\\braket\s*\{([^}]+)\}\s*\{([^}]+)\}/\\langle $1 | $2 \\rangle/g;
    return $content;
}

sub fix_file {
    my ($filepath) = @_;

    open(my $fh, '<:utf8', $filepath) or do {
        print "  ERROR: Cannot open $filepath: $!\n";
        return 0;
    };
    my $content = do { local $/; <$fh> };
    close($fh);

    my $original = $content;
    my @reasons;

    # Fix 1: Add \pdfoutput=1 as first line (before \documentclass)
    if ($content !~ /^\\pdfoutput=1/) {
        if ($content =~ /(\\documentclass)/) {
            my $pos = $-[0];
            my $line_start = rindex($content, "\n", $pos);
            if ($line_start == -1) {
                $content = "\\pdfoutput=1\n" . $content;
            } else {
                $content = substr($content, 0, $line_start) . "\n\\pdfoutput=1\n" . substr($content, $line_start);
            }
            push @reasons, 'pdfoutput=1';
        } else {
            # No \documentclass found, prepend anyway
            $content = "\\pdfoutput=1\n" . $content;
            push @reasons, 'pdfoutput=1 (no documentclass)';
        }
    }

    # Fix 2: Remove \usepackage[utf8]{inputenc}
    if ($content =~ s/\\usepackage\[utf8?\]\{inputenc\}\s*\n?//g) {
        push @reasons, 'remove inputenc';
    }
    $content =~ s/\\usepackage\{inputenc\}\s*\n?//g;

    # Fix 3: Remove \usepackage{physics} & replace physics commands
    if ($content =~ /\\usepackage\{physics\}/) {
        $content = replace_physics_cmds($content);
        $content =~ s/\\usepackage\{physics\}\s*\n?//g;
        push @reasons, 'remove physics';
    }

    # Fix 4: Remove linkcolor=blue from hyperref options
    if ($content =~ /linkcolor\s*=\s*blue/) {
        $content =~ s/linkcolor\s*=\s*blue\s*,?\s*//g;
        $content =~ s/,?\s*linkcolor\s*=\s*blue//g;
        push @reasons, 'remove linkcolor=blue';
    }

    # Fix 5: \documentclass{ctexart} → \documentclass{article}
    if ($content =~ /ctexart/) {
        $content =~ s/\\documentclass\{ctexart\}/\\documentclass{article}/g;
        $content =~ s/\\documentclass\[([^\]]*)\]\{ctexart\}/\\documentclass[$1]{article}/g;
        push @reasons, 'ctexart→article';
    }

    # Remove ctex/xeCJK/fontspec/CJK related packages
    for my $pkg (qw(ctex xeCJK fontspec CJK CJKutf8 CJKspace)) {
        if ($content =~ s/\\usepackage(?:\[[^\]]*\])?\{$pkg\}\s*\n?//g) {
            push @reasons, "remove $pkg" unless grep { $_ eq "remove $pkg" } @reasons;
        }
    }

    # Fix 6: \author{...} → \author{SCX}
    if ($content =~ s/\\author\{[^}]*\}/\\author{SCX}/g) {
        push @reasons, 'author→SCX';
    }

    if ($content ne $original) {
        open(my $out_fh, '>:utf8', $filepath) or die "Cannot write $filepath: $!";
        print $out_fh $content;
        close($out_fh);
        print "  FIXED: $filepath  [" . join(', ', @reasons) . "]\n";
        return 1;
    } else {
        print "  SKIP:  $filepath  [no changes needed]\n";
        return 0;
    }
}

my $total = scalar(@FILES);
my $count = 0;
print "Processing $total supplementary .tex files...\n\n";
foreach my $f (@FILES) {
    $count += fix_file($f);
}
print "\nTotal: $count files modified out of $total\n";
