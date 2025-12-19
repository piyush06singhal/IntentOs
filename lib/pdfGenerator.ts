// Generate a beautiful PDF report from analysis results
export function generatePDFReport(results: any, userInput: string) {
  // Create a new window with the report content
  const printWindow = window.open('', '_blank')
  
  if (!printWindow) {
    alert('Please allow popups to download the PDF')
    return
  }

  const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>IntentOS Analysis Report</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.6;
      color: #333;
      padding: 40px;
      max-width: 900px;
      margin: 0 auto;
    }
    .header {
      text-align: center;
      margin-bottom: 40px;
      padding-bottom: 20px;
      border-bottom: 3px solid #8b5cf6;
    }
    .logo {
      font-size: 36px;
      font-weight: bold;
      background: linear-gradient(135deg, #8b5cf6, #3b82f6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 10px;
    }
    .subtitle {
      color: #666;
      font-size: 14px;
    }
    .section {
      margin-bottom: 30px;
      page-break-inside: avoid;
    }
    .section-title {
      font-size: 24px;
      font-weight: bold;
      color: #8b5cf6;
      margin-bottom: 15px;
      padding-bottom: 10px;
      border-bottom: 2px solid #e5e7eb;
    }
    .subsection-title {
      font-size: 18px;
      font-weight: 600;
      color: #3b82f6;
      margin: 20px 0 10px 0;
    }
    .card {
      background: #f9fafb;
      border-left: 4px solid #8b5cf6;
      padding: 15px;
      margin: 10px 0;
      border-radius: 4px;
    }
    .badge {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
      margin: 5px 5px 5px 0;
    }
    .badge-primary { background: #ddd6fe; color: #6d28d9; }
    .badge-success { background: #d1fae5; color: #065f46; }
    .badge-warning { background: #fef3c7; color: #92400e; }
    .badge-danger { background: #fee2e2; color: #991b1b; }
    .step {
      background: white;
      border: 1px solid #e5e7eb;
      padding: 15px;
      margin: 15px 0;
      border-radius: 8px;
      page-break-inside: avoid;
    }
    .step-number {
      display: inline-block;
      width: 30px;
      height: 30px;
      background: linear-gradient(135deg, #8b5cf6, #3b82f6);
      color: white;
      border-radius: 50%;
      text-align: center;
      line-height: 30px;
      font-weight: bold;
      margin-right: 10px;
    }
    .step-title {
      font-size: 16px;
      font-weight: 600;
      color: #1f2937;
      margin-bottom: 8px;
    }
    .step-description {
      color: #4b5563;
      margin-bottom: 10px;
    }
    .step-meta {
      font-size: 13px;
      color: #6b7280;
      margin-top: 10px;
    }
    .confidence-bar {
      height: 20px;
      background: #e5e7eb;
      border-radius: 10px;
      overflow: hidden;
      margin: 10px 0;
    }
    .confidence-fill {
      height: 100%;
      background: linear-gradient(90deg, #10b981, #3b82f6);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 12px;
      font-weight: bold;
    }
    .footer {
      margin-top: 50px;
      padding-top: 20px;
      border-top: 2px solid #e5e7eb;
      text-align: center;
      color: #6b7280;
      font-size: 12px;
    }
    ul { margin-left: 20px; margin-top: 10px; }
    li { margin: 5px 0; }
    @media print {
      body { padding: 20px; }
      .no-print { display: none; }
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="logo">IntentOS</div>
    <div class="subtitle">AI Decision Intelligence Report • Generated ${new Date().toLocaleDateString()}</div>
  </div>

  <div class="section">
    <div class="section-title">📝 Your Goal</div>
    <div class="card">
      <p><strong>${userInput}</strong></p>
    </div>
  </div>

  ${results.intent ? `
  <div class="section">
    <div class="section-title">🎯 Intent Analysis</div>
    
    <div class="subsection-title">Primary Goal</div>
    <div class="card">
      <p><strong>${results.intent.primary_intent?.goal || results.intent.primary_intent}</strong></p>
      <div style="margin-top: 10px;">
        <span class="badge badge-primary">${results.intent.primary_intent?.category || 'General'}</span>
        ${results.intent.primary_intent?.confidence ? `
          <div class="confidence-bar" style="margin-top: 10px;">
            <div class="confidence-fill" style="width: ${results.intent.primary_intent.confidence * 100}%">
              ${Math.round(results.intent.primary_intent.confidence * 100)}% Confidence
            </div>
          </div>
        ` : ''}
      </div>
    </div>

    ${results.intent.secondary_intents && results.intent.secondary_intents.length > 0 ? `
      <div class="subsection-title">Secondary Goals</div>
      ${results.intent.secondary_intents.map((intent: any) => `
        <div class="card">
          <p>${intent.goal || intent}</p>
          ${intent.priority ? `<span class="badge badge-warning">${intent.priority} priority</span>` : ''}
        </div>
      `).join('')}
    ` : ''}

    ${results.intent.conflicts && results.intent.conflicts.length > 0 ? `
      <div class="subsection-title">⚠️ Detected Conflicts</div>
      ${results.intent.conflicts.map((conflict: any) => `
        <div class="card">
          <p><strong>${conflict.description}</strong></p>
          <p style="margin-top: 8px; color: #059669;"><strong>Resolution:</strong> ${conflict.resolution_strategy}</p>
          <span class="badge badge-danger">${conflict.severity} severity</span>
        </div>
      `).join('')}
    ` : ''}
  </div>
  ` : ''}

  ${results.constraints ? `
  <div class="section">
    <div class="section-title">⚙️ Constraints & Resources</div>
    <div class="card">
      ${results.constraints.time_constraint?.value ? `<p><strong>Time Available:</strong> ${results.constraints.time_constraint.value}</p>` : ''}
      ${results.constraints.skill_level?.current ? `<p><strong>Skill Level:</strong> ${results.constraints.skill_level.current}</p>` : ''}
      ${results.constraints.resources?.budget ? `<p><strong>Budget:</strong> ${results.constraints.resources.budget}</p>` : ''}
    </div>
  </div>
  ` : ''}

  ${results.plans?.candidate_plans ? `
  <div class="section">
    <div class="section-title">📋 Recommended Action Plan</div>
    <div class="card">
      <p><strong>Selected Plan:</strong> ${results.plans.recommended_plan?.replace('_', ' ') || 'Optimal'}</p>
      <p style="margin-top: 5px; color: #6b7280;">${results.plans.recommendation_reasoning || ''}</p>
    </div>

    ${results.plans.candidate_plans.find((p: any) => p.plan_id === results.plans.recommended_plan)?.plan.map((step: any, index: number) => `
      <div class="step">
        <div>
          <span class="step-number">${step.step_number || index + 1}</span>
          <span class="step-title">${step.title}</span>
        </div>
        <div class="step-description">${step.description}</div>
        ${step.estimated_time || step.success_criteria ? `
          <div class="step-meta">
            ${step.estimated_time ? `⏱️ ${step.estimated_time}` : ''}
            ${step.success_criteria ? `<br>✅ Success: ${step.success_criteria}` : ''}
          </div>
        ` : ''}
      </div>
    `).join('') || ''}

    ${results.plans.risks && results.plans.risks.length > 0 ? `
      <div class="subsection-title">⚠️ Risk Analysis</div>
      ${results.plans.risks.map((risk: any) => `
        <div class="card">
          <p><strong>${risk.risk}</strong></p>
          <p style="margin-top: 8px; color: #059669;"><strong>Mitigation:</strong> ${risk.mitigation}</p>
          <span class="badge badge-warning">${risk.probability} probability</span>
          <span class="badge badge-danger">${risk.impact} impact</span>
        </div>
      `).join('')}
    ` : ''}
  </div>
  ` : ''}

  ${results.validation && !results.validation.is_valid ? `
  <div class="section">
    <div class="section-title">🛡️ Validation Notes</div>
    ${results.validation.feasibility_issues?.map((issue: any) => `
      <div class="card">
        <p><strong>Issue:</strong> ${issue.issue}</p>
        <p style="margin-top: 8px; color: #059669;"><strong>Recommendation:</strong> ${issue.recommendation}</p>
      </div>
    `).join('') || ''}
  </div>
  ` : ''}

  <div class="footer">
    <p><strong>IntentOS v2.1</strong> - AI Decision Intelligence System</p>
    <p style="margin-top: 5px;">Transform ambiguity into action • 5 Advanced AI Features</p>
    <p style="margin-top: 10px;">This report was generated using advanced AI analysis with multi-intent detection, constraint optimization, and validation guardrails.</p>
  </div>

  <div class="no-print" style="position: fixed; top: 20px; right: 20px; background: white; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <button onclick="window.print()" style="background: linear-gradient(135deg, #8b5cf6, #3b82f6); color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 14px;">
      📄 Save as PDF
    </button>
    <button onclick="window.close()" style="background: #e5e7eb; color: #374151; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; margin-left: 10px; font-size: 14px;">
      Close
    </button>
  </div>
</body>
</html>
  `

  printWindow.document.write(html)
  printWindow.document.close()
  
  // Auto-trigger print dialog after a short delay
  setTimeout(() => {
    printWindow.print()
  }, 500)
}
