#!/usr/bin/env python3
"""
Statutory Risk Scorer
Scores extracted legal clauses against internal playbook rules.
"""

from typing import Dict, Any, Tuple

class LegalRiskScorer:
    def __init__(self):
        pass

    def evaluate_clause_risk(self, clause: Dict[str, Any]) -> Tuple[str, float, str]:
        """
        Evaluate risk level for a single legal clause.
        Returns: (risk_level, risk_score, reason)
        """
        c_type = clause["type"]
        text = clause["text"].lower()

        if c_type == "indemnification":
            if "uncapped" in text or "sole discretion" in text or "hold harmless" in text:
                return "CRITICAL", 95.0, "Onerous uncapped indemnification clause detected."
            return "MEDIUM", 60.0, "Standard indemnification clause."

        elif c_type == "limitation_of_liability":
            if "exceed" not in text or "zero" in text:
                return "HIGH", 85.0, "Limitation of liability is severely restricted or un-capped."
            return "LOW", 30.0, "Standard liability limitation clause."

        elif c_type == "termination":
            if "without cause" in text or "without notice" in text:
                return "HIGH", 80.0, "Unilateral termination without notice detected."
            return "LOW", 25.0, "Standard mutual termination clause."

        return "LOW", 20.0, "Low risk standard clause."
