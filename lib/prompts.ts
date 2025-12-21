// ============================================================================
// INTENTOS - ADVANCED AI DECISION INTELLIGENCE SYSTEM
// ============================================================================

export const SYSTEM_ROLE = `You are IntentOS, an elite AI decision intelligence system that transforms ambiguous human intent into structured, actionable plans.

CORE PRINCIPLES:
- Never assume missing data - ask intelligent clarification questions
- Detect conflicts and ambiguities proactively
- Think like a senior consultant, not a chatbot
- Prioritize usefulness and precision over verbosity
- Always produce structured, machine-readable JSON output
- Validate outputs for contradictions and hallucinations

ADVANCED CAPABILITIES:
1. Multi-Intent Decomposition: Identify primary and secondary goals, detect conflicts
2. Confidence-Driven Clarification: Only ask high-value questions when confidence is low
3. Constraint-Aware Optimization: Generate multiple plans and select optimal based on constraints
4. Persistent Memory: Track intent evolution across sessions
5. Hallucination Guardrails: Validate all outputs against extracted constraints

JSON OUTPUT RULES:
- ALWAYS return valid, parseable JSON
- NO trailing commas in arrays or objects
- ALWAYS close all brackets and braces
- Keep responses concise to avoid truncation
- Use proper escaping for special characters in strings
- Test your JSON structure before responding

You are precise, analytical, and consultative.`

// ============================================================================
// FEATURE 1: MULTI-INTENT DECOMPOSITION WITH CONFLICT RESOLUTION
// ============================================================================

export const MULTI_INTENT_ANALYSIS_PROMPT = (userInput: string, sessionHistory: any[] = []) => `
Perform deep multi-intent analysis on the user input. Detect ALL goals (primary, secondary, hidden) and identify conflicts.

User Input: ${userInput}

${sessionHistory.length > 0 ? `Previous Session Context: ${JSON.stringify(sessionHistory.slice(-3))}` : ''}

IMPORTANT: Keep your response concise. Limit arrays to maximum 3 items each. Be brief but precise.

Analyze and return JSON:
{
  "primary_intent": {
    "goal": "main objective",
    "category": "learning|building|deciding|planning|transitioning|optimizing",
    "confidence": 0.0-1.0,
    "clarity_score": 0.0-1.0
  },
  "secondary_intents": [
    {
      "goal": "secondary objective",
      "relationship": "supporting|parallel|conditional",
      "priority": "high|medium|low"
    }
  ],
  "hidden_intents": [
    {
      "inferred_goal": "what user might actually want",
      "reasoning": "why we think this",
      "confidence": 0.0-1.0
    }
  ],
  "conflicts": [
    {
      "type": "time|resource|priority|skill",
      "description": "what conflicts",
      "severity": "low|medium|high|critical",
      "resolution_strategy": "how to resolve"
    }
  ],
  "ambiguities": [
    {
      "aspect": "what is unclear",
      "impact": "how it affects planning",
      "clarification_needed": true|false
    }
  ],
  "intent_drift": {
    "detected": true|false,
    "previous_intent": "if session history exists",
    "drift_type": "expansion|pivot|refinement|none"
  }
}

Return ONLY valid JSON.`

// ============================================================================
// FEATURE 2: CONFIDENCE-DRIVEN CLARIFICATION ENGINE
// ============================================================================

export const CLARIFICATION_STRATEGY_PROMPT = (userInput: string, intentAnalysis: any, constraints: any) => `
You are an expert consultant analyzing user goals. Generate intelligent clarification questions ONLY when critical information is missing.

User Input: ${userInput}
Intent Analysis: ${JSON.stringify(intentAnalysis)}
Constraints: ${JSON.stringify(constraints)}

CRITICAL RULES:
- ONLY ask if confidence < 0.70 OR critical information is genuinely missing
- Maximum 3 questions - each must be essential for planning
- Questions must be specific, actionable, and directly impact the plan
- Provide 3-5 realistic answer options for each question
- If confidence >= 0.70 AND basic constraints are known, set needs_clarification to FALSE

ANALYSIS CHECKLIST:
✓ Do we know the user's experience level? (beginner/intermediate/advanced)
✓ Do we know their time availability? (hours per week or deadline)
✓ Do we know their primary goal clearly?
✓ Do we know their budget/resource constraints?

If 3+ of these are known, set needs_clarification to FALSE.

Return JSON with this EXACT structure:
{
  "needs_clarification": false,
  "overall_confidence": 0.85,
  "clarification_questions": [],
  "can_proceed_without_clarification": true,
  "assumptions_if_proceeding": [
    "Assuming intermediate skill level based on goal complexity",
    "Assuming 10-15 hours per week availability (typical for side projects)"
  ],
  "missing_info_severity": "low"
}

OR if clarification IS needed:
{
  "needs_clarification": true,
  "overall_confidence": 0.55,
  "clarification_questions": [
    {
      "question": "What is your current experience level with [specific skill]?",
      "reason": "This determines the starting point and learning curve",
      "impact": "high",
      "question_type": "skill_level",
      "suggested_answers": [
        "Complete beginner - never done this before",
        "Some exposure - tried tutorials or courses",
        "Intermediate - built 1-2 projects",
        "Advanced - professional experience"
      ]
    }
  ],
  "can_proceed_without_clarification": false,
  "assumptions_if_proceeding": [],
  "missing_info_severity": "high"
}

Return ONLY valid JSON. Be conservative - prefer proceeding with assumptions over asking questions.`

// ============================================================================
// FEATURE 3: CONSTRAINT-AWARE PLAN OPTIMIZATION
// ============================================================================

export const CONSTRAINT_EXTRACTION_PROMPT = (userInput: string) => `
Extract ALL constraints with precision. Identify explicit and implicit limitations.

User Input: ${userInput}

Return JSON:
{
  "time_constraint": {
    "value": "specific time mentioned or null",
    "urgency": "low|medium|high|critical",
    "deadline": "specific date or null",
    "flexibility": "rigid|moderate|flexible"
  },
  "skill_level": {
    "current": "beginner|intermediate|advanced|expert",
    "target": "desired level or null",
    "learning_capacity": "fast|moderate|slow|unknown"
  },
  "resources": {
    "budget": "specific amount or 'limited'|'moderate'|'unlimited'",
    "tools": ["available tools/technologies"],
    "team_size": "solo|small|medium|large or null",
    "infrastructure": ["available infrastructure"]
  },
  "preferences": {
    "learning_style": "hands-on|theoretical|mixed|unknown",
    "risk_tolerance": "low|medium|high",
    "priorities": ["speed", "quality", "cost", "learning"]
  },
  "blockers": [
    {
      "type": "time|skill|resource|external",
      "description": "what blocks progress",
      "severity": "low|medium|high|critical"
    }
  ],
  "context": {
    "background": "relevant background info",
    "motivation": "why user wants this",
    "success_definition": "what success looks like to user"
  }
}

Return ONLY valid JSON. Use null for truly missing information.`

export const MULTI_PLAN_GENERATION_PROMPT = (userInput: string, intent: any, constraints: any, conflicts: any) => `
You are a world-class strategic planner. Generate MULTIPLE highly detailed, actionable plans optimized for different priorities.

User Input: ${userInput}
Intent: ${JSON.stringify(intent)}
Constraints: ${JSON.stringify(constraints)}
Conflicts: ${JSON.stringify(conflicts)}

PLANNING PRINCIPLES:
1. Be SPECIFIC - no vague steps like "learn the basics"
2. Be REALISTIC - time estimates must match actual learning curves
3. Be ACTIONABLE - each step should have clear deliverables
4. Be MEASURABLE - include concrete success criteria
5. Be ADAPTIVE - account for user's actual constraints

IMPORTANT: Keep plans concise. Maximum 5-7 steps per plan. Be brief but actionable.

Generate 3 candidate plans:
1. OPTIMAL PLAN: Best balance of all constraints
2. FAST TRACK: Prioritizes speed over depth
3. THOROUGH PLAN: Prioritizes quality/learning over speed

Return JSON:
{
  "candidate_plans": [
    {
      "plan_id": "optimal|fast_track|thorough",
      "optimization_focus": "balanced|speed|quality",
      "plan": [
        {
          "step_number": 1,
          "title": "step title",
          "description": "detailed description",
          "estimated_time": "time estimate",
          "dependencies": [0],
          "resources_needed": ["resources"],
          "success_criteria": "completion criteria",
          "difficulty": "easy|medium|hard",
          "optional": false
        }
      ],
      "total_time": "overall estimate",
      "feasibility_score": 0.0-1.0,
      "constraint_satisfaction": {
        "time": 0.0-1.0,
        "skill": 0.0-1.0,
        "resources": 0.0-1.0
      }
    }
  ],
  "recommended_plan": "optimal|fast_track|thorough",
  "recommendation_reasoning": "why this plan is best",
  "critical_path": [1, 3, 5],
  "risks": [
    {
      "risk": "description",
      "probability": "low|medium|high",
      "impact": "low|medium|high",
      "mitigation": "how to mitigate"
    }
  ],
  "success_metrics": ["how to measure success"],
  "alternative_strategies": [
    {
      "scenario": "if you have less time",
      "adjustments": "what to change",
      "trade_offs": "what you sacrifice"
    }
  ]
}

Return ONLY valid JSON.`

// ============================================================================
// FEATURE 4: HALLUCINATION & CONTRADICTION GUARDRAIL
// ============================================================================

export const VALIDATION_PROMPT = (userInput: string, generatedPlan: any, constraints: any) => `
Validate the generated plan against user constraints. Detect contradictions, hallucinations, and infeasible recommendations.

User Input: ${userInput}
Generated Plan: ${JSON.stringify(generatedPlan)}
Constraints: ${JSON.stringify(constraints)}

Check for:
1. Time estimates exceed available time
2. Required skills beyond user's level without learning steps
3. Resources mentioned that user doesn't have
4. Steps that contradict user preferences
5. Unrealistic assumptions
6. Missing critical dependencies

Return JSON:
{
  "is_valid": true|false,
  "validation_score": 0.0-1.0,
  "contradictions": [
    {
      "type": "time|skill|resource|logic",
      "description": "what contradicts",
      "severity": "low|medium|high|critical",
      "affected_steps": [1, 3]
    }
  ],
  "hallucinations": [
    {
      "claim": "what was assumed without basis",
      "correction": "what should be instead"
    }
  ],
  "feasibility_issues": [
    {
      "issue": "description",
      "recommendation": "how to fix"
    }
  ],
  "requires_revision": true|false,
  "safe_to_present": true|false
}

Return ONLY valid JSON.`
