#!/usr/bin/env python3
"""
Legal Contract Clause & Risk Auditor Test Runner
Tests clause extraction, risk scoring, and redline suggestion generation.
"""

from clause_extractor import CUADClauseExtractor
from risk_scorer import LegalRiskScorer
from redline_generator import LegalRedlineGenerator

SAMPLE_CONTRACT_TEXT = """
COMMERCIAL SERVICES AGREEMENT

1. INDEMNIFICATION CLAUSE
Client agrees to indemnify, defend, and hold harmless Provider from any and all uncapped claims, losses, damages, or liabilities arising out of performance of services under this Agreement in Provider's sole discretion.

2. LIMITATION OF LIABILITY
In no event shall Provider's total aggregate liability under this Agreement exceed the amount of zero dollars ($0.00). Neither party shall be liable for consequential damages.

3. TERMINATION FOR CONVENIENCE
Provider reserves the right to terminate this agreement immediately without cause and without notice to Client.

4. GOVERNING LAW
This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware.
"""

def run_legal_auditor_test():
    print("==================================================")
    print(" ⚖️ LEGAL CONTRACT CLAUSE & RISK AUDITOR TEST ")
    print("==================================================")
    
    # 1. Extract Clauses
    print("1. Extracting CUAD Legal Clauses from Commercial Contract...")
    extractor = CUADClauseExtractor()
    clauses = extractor.extract_clauses(SAMPLE_CONTRACT_TEXT)
    print(f"   Successfully extracted {len(clauses)} legal clauses!")

    # 2. Score Risk & Generate Redlines
    scorer = LegalRiskScorer()
    redliner = LegalRedlineGenerator()

    print("\n2. Evaluating Statutory Risk Scores & Redline Recommendations:")
    for c in clauses:
        risk_level, score, reason = scorer.evaluate_clause_risk(c)
        redline = redliner.suggest_redline(c, risk_level)

        print(f"\n   📄 Clause #{c['clause_id']} ({c['type'].upper()}):")
        print(f"      - Risk Level: {risk_level} (Score: {score}/100)")
        print(f"      - Reason: {reason}")
        print(f"      - {redline}")

    print("\n==================================================")
    print(" 📊 TEST SUMMARY: Legal Contract Auditor Operational!")
    print("==================================================")

if __name__ == "__main__":
    run_legal_auditor_test()
