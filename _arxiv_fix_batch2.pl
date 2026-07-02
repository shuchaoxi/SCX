#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use Encode;

my @FILES = (
    "papers/scx_prize/scx_prize.tex",
    "papers/scx_protocol_governance/protocol_governance.tex",
    "papers/scx_pseudopotential/main.tex",
    "papers/scx_qg_audit/main.tex",
    "papers/scx_quant_finance/main.tex",
    "papers/scx_quantum/main.tex",
    "papers/scx_quantum_audit/quantum_audit.tex",
    "papers/scx_resistance/resistance_paradox.tex",
    "papers/scx_review/main.tex",
    "papers/scx_review/supp.tex",
    "papers/scx_S_operator/S_operator.tex",
    "papers/scx_science_audit/main.tex",
    "papers/scx_security/main.tex",
    "papers/scx_singularity/singularity_theory.tex",
    "papers/scx_social_media/social_gauge.tex",
    "papers/scx_spring_framework/spring_framework.tex",
    "papers/scx_spring_limits/spring_limits.tex",
    "papers/scx_spring_md/spring_md.tex",
    "papers/scx_spring_trainer/spring_trainer.tex",
    "papers/scx_string_unified/main.tex",
    "papers/scx_supplementary_docs/main.tex",
    "papers/scx_supply_chain/main.tex",
    "papers/scx_temporal/main.tex",
    "papers/scx_theory/main.tex",
    "papers/scx_theory/S1_thm1_noise_detection.tex",
    "papers/scx_theory/S2_thm2_weak_features.tex",
    "papers/scx_theory/S3_thm3_unidentifiability.tex",
    "papers/scx_theory/S4_thm4_exact_constant_minimax.tex",
    "papers/scx_theory/S5_thm5_cluster_consistency.tex",
    "papers/scx_theory/S6_prop6_bootstrap_stability.tex",
    "papers/scx_theory/S7_experimental_details.tex",
    "papers/scx_theory/S8_numerical_verification.tex",
    "papers/scx_turbulence/main.tex",
    "papers/scx_turbulence_moduli/main.tex",
    "papers/scx_turbulence_moduli/main_staged.tex",
    "papers/scx_unified_field/main.tex",
    "papers/scx_world_government/world_government.tex",
    "papers/scx_world_model/main.tex",
    "papers/situs_applications/main.tex",
    "papers/situs_theory/main.tex",
    "papers/spring_config/main.tex",
    "papers/taxonomic_nn/main.tex",
    "papers/taxonomic_nn/theorem3.tex",
    "papers/taxonomic_nn/theorem3_short.tex",
    "papers/theorems/theorem_2_weak_feature.tex",
    "papers/theorems/theorem_aa_alignment.tex",
    "papers/theorems/theorem_ac_complexity.tex",
    "papers/theorems/theorem_ae_entropy.tex",
    "papers/theorems/theorem_ar_adversarial.tex",
    "papers/theorems/theorem_cd_causal.tex",
    "papers/theorems/theorem_fa_federated.tex",
    "papers/theorems/theorem_hc_human.tex",
    "papers/theorems/theorem_q_quantum.tex",
    "papers/theorems/theorem_ra_recursive.tex",
    "papers/theorems/theorem_ts_temporal.tex",
    "papers/theorems/theorem5_active_learning.tex",
    "papers/theorems/theorem6_protocol_game.tex",
    "papers/theorems/theorem7_cross_domain.tex",
    "papers/yajie_protocol/human_future.tex",
    "papers/yajie_protocol/main.tex",
);

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

    # Fix 1: Add \pdfoutput=1 before \documentclass
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
        }
    }

    # Fix 2: Remove \usepackage[utf8]{inputenc}
    if ($content =~ s/\\usepackage\[utf8?\]\{inputenc\}\s*\n?//g) {
        push @reasons, 'remove inputenc';
    }
    $content =~ s/\\usepackage\{inputenc\}\s*\n?//g;

    # Fix 3: Remove \usepackage{physics} & replace physics commands
    if ($content =~ /\\usepackage\{physics\}/) {
        # Replace physics commands first
        $content =~ s/\\dv\s*\{([^}]+)\}\s*\{([^}]+)\}/\\frac{d $1}{d $2}/g;
        $content =~ s/\\dv\*\s*\{([^}]+)\}\s*\{([^}]+)\}/\\frac{d $1}{d $2}/g;
        $content =~ s/\\pdv\s*\{([^}]+)\}\s*\{([^}]+)\}/\\frac{\\partial $1}{\\partial $2}/g;
        $content =~ s/\\pdv\*\s*\{([^}]+)\}\s*\{([^}]+)\}/\\frac{\\partial $1}{\\partial $2}/g;
        $content =~ s/\\abs\s*\{([^}]+)\}/\\left|$1\\right|/g;
        $content =~ s/\\norm\s*\{([^}]+)\}/\\left\\|$1\\right\\|/g;
        $content =~ s/\\ket\s*\{([^}]+)\}/|$1\\rangle/g;
        $content =~ s/\\bra\s*\{([^}]+)\}/\\langle $1|/g;
        $content =~ s/\\braket\s*\{([^}]+)\}\s*\{([^}]+)\}/\\langle $1 | $2 \\rangle/g;

        # Then remove the package
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
    if ($content =~ s/\\usepackage(?:\[[^\]]*\])?\{ctex\}\s*\n?//g)  { push @reasons, 'remove ctex'; }
    if ($content =~ s/\\usepackage(?:\[[^\]]*\])?\{xeCJK\}\s*\n?//g) { push @reasons, 'remove xeCJK'; }
    if ($content =~ s/\\usepackage(?:\[[^\]]*\])?\{fontspec\}\s*\n?//g) { push @reasons, 'remove fontspec'; }
    $content =~ s/\\usepackage(?:\[[^\]]*\])?\{CJK(?:utf8|space)?\}\s*\n?//g;

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
print "Processing $total files...\n\n";
foreach my $f (@FILES) {
    $count += fix_file($f);
}
print "\nTotal: $count files modified out of $total\n";
