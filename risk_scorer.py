#!/usr/bin/env python3
"""
Statutory Risk Scorer with Google Gemini LLM Integration
Scores extracted legal clauses against CUAD benchmark legal rules and generates attorney redlines.
"""

import os
import json
from typing import Dict, Any, Tuple
from dotenv import load_dotenv

load_dotenv("/Users/apple/Documents/Zero_fks/.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

class LegalRiskScorer:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
            except Exception as e:
                self.model = None
        else:
            self.model = None

    def evaluate_clause_risk(self, clause: Dict[str, Any]) -> Tuple[str, float, str]:
        """
        Evaluate risk level for a single legal clause using Gemini LLM with fallback rules.
        Returns: (risk_level, risk_score, reason)
        """
        c_type = clause.get("type", "general")
        text = clause.get("text", "")

        # Use Gemini LLM if configured
        if self.model:
            try:
                prompt = f"""
                Analyze the following legal contract clause as an expert corporate attorney:
                Clause Type: {c_type}
                Clause Text: "{text}"

                Return a JSON object with:
                - "risk_level": "CRITICAL", "HIGH", "MEDIUM", or "LOW"
                - "risk_score": float between 0.0 and 100.0
                - "reason": detailed one-sentence explanation of the liability risk and recommended redline edit.
                """
                response = self.model.generate_content(prompt)
                res_text = response.text
                
                # Parse JSON
                if "{" in res_text and "}" in res_text:
                    json_str = res_text[res_text.find("{"):res_text.rfind("}")+1]
                    data = json.loads(json_str)
                    return data.get("risk_level", "HIGH"), float(data.get("risk_score", 85.0)), data.get("reason", "LLM-identified contract liability risk.")
            except Exception as e:
                pass

        # Robust Fallback Rule Engine
        text_lower = text.lower()
        if c_type == "indemnification":
            if any(k in text_lower for k in ["uncapped", "sole discretion", "hold harmless", "defend"]):
                return "CRITICAL", 95.0, "Onerous uncapped indemnification clause detected. Recommend adding mutual liability cap."
            return "MEDIUM", 60.0, "Standard indemnification clause."

        elif c_type == "limitation_of_liability":
            if any(k in text_lower for k in ["exceed", "zero", "unlimited", "consequential"]):
                return "HIGH", 85.0, "Limitation of liability is restricted or un-capped. Recommend capping liability to 12 months fees."
            return "LOW", 30.0, "Standard liability limitation clause."

        elif c_type == "termination":
            if any(k in text_lower for k in ["without cause", "without notice", "immediate"]):
                return "HIGH", 80.0, "Unilateral termination without notice detected. Recommend 30-day notice requirement."
            return "LOW", 25.0, "Standard mutual termination clause."

        return "LOW", 20.0, "Low risk standard commercial clause."
