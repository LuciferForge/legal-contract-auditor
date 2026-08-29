#!/usr/bin/env python3
"""
Redline & Reasoning Generator
Generates concrete legal redline recommendations for high-risk clauses.
"""

from typing import Dict, Any

class LegalRedlineGenerator:
    def __init__(self):
        pass

    def suggest_redline(self, clause: Dict[str, Any], risk_level: str) -> str:
        """Suggest redline wording for high-risk clauses"""
        c_type = clause["type"]

        if risk_level in ["CRITICAL", "HIGH"]:
            if c_type == "indemnification":
                return "SUGGESTED REDLINE: Insert cap on indemnification liability equal to 1x annual contract fees paid."
            elif c_type == "limitation_of_liability":
                return "SUGGESTED REDLINE: Ensure mutual liability cap applies equally to both Provider and Client."
            elif c_type == "termination":
                return "SUGGESTED REDLINE: Require at least 30 days prior written notice for termination for convenience."

        return "NO REDLINE REQUIRED: Clause meets standard legal risk thresholds."
