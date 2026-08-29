#!/usr/bin/env python3
"""
CUAD Clause Extractor
Identifies and extracts key legal clauses (Indemnification, Liability, Termination, Governing Law).
"""

import re
from typing import List, Dict, Any

CLAUSE_PATTERNS = {
    "indemnification": re.compile(r"(indemnify|indemnification|hold harmless)", re.IGNORECASE),
    "limitation_of_liability": re.compile(r"(limitation of liability|aggregate liability|consequential damages)", re.IGNORECASE),
    "termination": re.compile(r"(termination for convenience|right to terminate|terminate this agreement)", re.IGNORECASE),
    "governing_law": re.compile(r"(governing law|jurisdiction|venue|laws of)", re.IGNORECASE)
}

class CUADClauseExtractor:
    def __init__(self):
        pass

    def extract_clauses(self, contract_text: str) -> List[Dict[str, Any]]:
        """Extract structured legal clauses from contract text"""
        paragraphs = [p.strip() for p in contract_text.split("\n\n") if len(p.strip()) > 20]
        extracted = []

        for idx, p in enumerate(paragraphs, 1):
            for clause_type, pattern in CLAUSE_PATTERNS.items():
                if pattern.search(p):
                    extracted.append({
                        "clause_id": idx,
                        "type": clause_type,
                        "text": p
                    })

        return extracted
