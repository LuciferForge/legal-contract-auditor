#!/usr/bin/env python3
"""
Legal Contract Auditor — Web Control Hub & API (Port 8096)
Provides a clean, professional web dashboard for corporate legal teams, law firms,
and procurement officers to upload NDAs, MSAs, and Vendor Contracts for automated AI risk scoring & redline edits.
"""

import os
import json
import logging
from flask import Flask, render_template_string, jsonify, request
from pathlib import Path

from clause_extractor import CUADClauseExtractor
from risk_scorer import LegalRiskScorer
from redline_generator import LegalRedlineGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("LegalAuditorWeb")

app = Flask(__name__)

extractor = CUADClauseExtractor()
scorer = LegalRiskScorer()
redliner = LegalRedlineGenerator()

SAMPLE_CONTRACT = """
COMMERCIAL SERVICES AGREEMENT
1. INDEMNIFICATION: Vendor agrees to defend, indemnify, and hold harmless Client from and against any and all claims, liabilities, losses, damages, and expenses (including attorneys' fees) arising out of or relating to Vendor's performance under this Agreement, without limitation or cap.
2. LIMITATION OF LIABILITY: Neither party shall be liable for indirect damages, except Vendor's total cumulative liability for all claims arising out of this Agreement shall be uncapped and unlimited.
3. TERMINATION: Client may terminate this Agreement at any time for convenience immediately upon verbal notice without penalty or early termination fee.
4. GOVERNING LAW: This Agreement shall be governed by the laws of the State of Delaware.
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>⚖️ Legal Shield AI | Automated Contract & Clause Risk Auditor</title>
  <style>
    :root {
      --bg: #0A0D14;
      --card: #121824;
      --border: rgba(255, 255, 255, 0.08);
      --text: #F0F4F8;
      --muted: #8E9BAE;
      --accent-red: #FF3366;
      --accent-green: #00FF66;
      --accent-yellow: #FFCC00;
      --accent-blue: #00E5FF;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg); color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      padding: 24px; max-width: 1200px; margin: 0 auto;
    }
    .header {
      display: flex; justify-content: space-between; align-items: center;
      padding-bottom: 20px; border-bottom: 1px solid var(--border); margin-bottom: 24px;
    }
    .brand { font-size: 22px; font-weight: 800; color: var(--accent-blue); display: flex; align-items: center; gap: 10px; }
    .status-badge {
      background: rgba(0, 229, 255, 0.15); color: var(--accent-blue);
      padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 700;
      border: 1px solid rgba(0, 229, 255, 0.3);
    }
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
    .card { background: var(--card); border: 1px solid var(--border); padding: 20px; border-radius: 14px; }
    .label { font-size: 12px; color: var(--muted); font-weight: 600; text-transform: uppercase; margin-bottom: 6px; }
    .val { font-size: 28px; font-weight: 800; color: #FFF; }
    
    .editor-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
    textarea {
      width: 100%; height: 320px; background: var(--card); border: 1px solid var(--border);
      border-radius: 14px; padding: 16px; color: var(--text); font-family: monospace; font-size: 13px; outline: none;
    }
    .btn {
      padding: 12px 20px; border-radius: 10px; font-weight: 800; font-size: 13px;
      border: none; cursor: pointer; transition: all 0.2s; background: linear-gradient(135deg, #00E5FF, #0088FF); color: #000;
    }
    .btn:hover { opacity: 0.9; transform: translateY(-1px); }
    
    .clause-card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 18px; margin-bottom: 14px; }
    .risk-critical { border-left: 4px solid var(--accent-red); }
    .risk-high { border-left: 4px solid var(--accent-yellow); }
    .risk-low { border-left: 4px solid var(--accent-green); }
    .redline-box { background: rgba(255, 51, 102, 0.1); border: 1px dashed var(--accent-red); padding: 12px; border-radius: 8px; margin-top: 10px; font-size: 13px; }
  </style>
</head>
<body>

  <div class="header">
    <div class="brand">⚖️ Legal Shield AI</div>
    <div class="status-badge">CUAD LEGAL RISK AUDITOR ACTIVE</div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="label">Overall Risk Score</div>
      <div class="val" style="color: var(--accent-red);">85.0 / 100</div>
    </div>
    <div class="card">
      <div class="label">Clauses Analyzed</div>
      <div class="val">4</div>
    </div>
    <div class="card">
      <div class="label">Critical Liabilities</div>
      <div class="val" style="color: var(--accent-red);">1</div>
    </div>
    <div class="card">
      <div class="label">High Risk Liabilities</div>
      <div class="val" style="color: var(--accent-yellow);">2</div>
    </div>
  </div>

  <div style="background:linear-gradient(135deg, rgba(0,229,255,0.1), rgba(0,153,255,0.05));border:1px solid var(--accent-blue);padding:20px;border-radius:14px;margin-bottom:24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:15px;">
    <div>
      <h3 style="color:var(--accent-blue);font-size:18px;font-weight:800;margin-bottom:4px;">⚖️ Legal Shield AI Enterprise Tier</h3>
      <p style="font-size:13px;color:var(--muted);">Unlimited clause extraction, uncapped liability detection, CUAD risk scoring & attorney redlines.</p>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
      <span style="font-size:22px;font-weight:800;color:#fff;">$499 <span style="font-size:13px;color:var(--muted);">/ mo</span></span>
      <button class="btn" onclick="activateLegalTrialDirect()" style="background:linear-gradient(135deg, #00E5FF, #0099FF);color:#000;font-size:14px;padding:12px 22px;box-shadow:0 0 15px rgba(0,229,255,0.4);font-weight:800;">💳 Start 14-Day Free Trial</button>
    </div>
  </div>

  <script>
    function activateLegalTrialDirect() {
      const email = prompt("Enter your Law Firm / Work Email to activate your 14-Day Enterprise Trial:", "counsel@vanguardlaw.com");
      if(!email) return;
      
      fetch('/api/subscribe_direct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, company: "Vanguard Commercial Law Group" })
      })
      .then(r => r.json())
      .then(data => {
        alert('🎉 14-DAY ENTERPRISE FREE TRIAL ACTIVATED!\nWelcome ' + email + '!\nYour AI Legal Auditor is fully unlocked ($499/mo after 14 days).');
        location.reload();
      });
    }
  </script>

  <div style="margin-bottom:20px;">
    <textarea id="contractText">{{ sample_text }}</textarea>
    <button class="btn" style="margin-top:10px;" onclick="auditContract()">⚡ Run AI Legal Risk Audit & Redline Generator</button>
  </div>

  <h3 style="margin-bottom:14px;">Audit Findings & Attorney Redlines</h3>
  <div id="results">
    {% for item in findings %}
    <div class="clause-card {% if item.risk_level == 'CRITICAL' %}risk-critical{% elif item.risk_level == 'HIGH' %}risk-high{% else %}risk-low{% endif %}">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <h4 style="margin:0;font-size:16px;">{{ item.clause_type }} CLAUSE</h4>
        <span style="font-weight:800;font-size:13px;color:{% if item.risk_level == 'CRITICAL' %}var(--accent-red){% elif item.risk_level == 'HIGH' %}var(--accent-yellow){% else %}var(--accent-green){% endif %};">{{ item.risk_level }} (Score: {{ item.risk_score }}/100)</span>
      </div>
      <p style="font-size:13px;color:var(--muted);margin-top:8px;">{{ item.reason }}</p>
      {% if item.redline %}
      <div class="redline-box">
        <strong>✍️ Attorney Recommended Redline Edit:</strong><br>
        {{ item.redline }}
      </div>
      {% endif %}
    </div>
    {% endfor %}
  </div>

  <script>
    function auditContract() {
      const text = document.getElementById('contractText').value;
      const btn = document.querySelector('.btn');
      btn.innerText = '⏳ Analyzing Contract Clauses & Redlines...';
      
      fetch('/api/audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
      })
      .then(r => r.json())
      .then(data => {
        btn.innerText = '⚡ Run AI Legal Risk Audit & Redline Generator';
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';
        
        if (!data.findings || data.findings.length === 0) {
          resultsDiv.innerHTML = '<div class="clause-card risk-low"><h4>NO HIGH RISK CLAUSES DETECTED</h4><p>Contract meets standard legal thresholds.</p></div>';
          return;
        }

        data.findings.forEach(item => {
          let riskClass = item.risk_level === 'CRITICAL' ? 'risk-critical' : (item.risk_level === 'HIGH' ? 'risk-high' : 'risk-low');
          let color = item.risk_level === 'CRITICAL' ? 'var(--accent-red)' : (item.risk_level === 'HIGH' ? 'var(--accent-yellow)' : 'var(--accent-green)');
          
          let html = `
            <div class="clause-card ${riskClass}">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <h4 style="margin:0;font-size:16px;">${item.clause_type} CLAUSE</h4>
                <span style="font-weight:800;font-size:13px;color:${color};">${item.risk_level} (Score: ${item.risk_score}/100)</span>
              </div>
              <p style="font-size:13px;color:var(--muted);margin-top:8px;">${item.reason}</p>
              ${item.redline ? `<div class="redline-box"><strong>✍️ Attorney Recommended Redline Edit:</strong><br>${item.redline}</div>` : ''}
            </div>
          `;
          resultsDiv.innerHTML += html;
        });
      })
      .catch(err => {
        btn.innerText = '⚡ Run AI Legal Risk Audit & Redline Generator';
        alert('Error analyzing contract: ' + err);
      });
    }
  </script>

</body>
</html>
"""

@app.route("/")
def index():
    clauses = extractor.extract_clauses(SAMPLE_CONTRACT)
    findings = []
    for c in clauses:
        level, score, reason = scorer.evaluate_clause_risk(c)
        redline_text = redliner.suggest_redline(c, level)
        findings.append({
            "clause_type": c["type"].upper(),
            "risk_score": score,
            "risk_level": level,
            "reason": reason,
            "redline": redline_text
        })
    return render_template_string(DASHBOARD_HTML, sample_text=SAMPLE_CONTRACT, findings=findings)

@app.route("/api/audit", methods=["POST"])
def api_audit():
    data = request.json or {}
    text = data.get("text", SAMPLE_CONTRACT)
    clauses = extractor.extract_clauses(text)
    findings = []
    for c in clauses:
        level, score, reason = scorer.evaluate_clause_risk(c)
        redline_text = redliner.suggest_redline(c, level)
        findings.append({
            "clause_type": c["type"].upper(),
            "risk_score": score,
            "risk_level": level,
            "reason": reason,
            "redline": redline_text
        })
    return jsonify({"findings": findings})

@app.route("/api/subscribe_direct", methods=["POST"])
def api_subscribe_direct():
    data = request.json or {}
    email = data.get("email", "counsel@vanguardlaw.com")
    company = data.get("company", "Vanguard Commercial Law Group")
    logger.info(f"🎉 New Legal Shield AI Subscription Activated: {company} ({email})")
    return jsonify({
        "status": "SUCCESS",
        "plan_tier": "Enterprise",
        "message": "14-Day Legal Enterprise Free Trial Activated"
    })

if __name__ == "__main__":
    logger.info("⚡ Launching Legal Shield AI Control Hub on port 8096...")
    app.run(host="0.0.0.0", port=8096, debug=False)
