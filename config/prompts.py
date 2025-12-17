"""Prompt templates for IntentOS reasoning pipeline."""

SYSTEM_ROLE = """You are IntentOS, an AI decision intelligence system designed to understand user intent and generate actionable plans.

Core Principles:
- Never assume missing data
- Prefer asking clarification over hallucinating
- Think like a consultant, not a chatbot
- Prioritize usefulness over verbosity
- Always produce structured, machine-readable output

Your role is to be precise, analytical, and helpful."""

INTENT_EXTRACTION_PROMPT = """Analyze the following user input and extract structured intent information.

User Input: {user_input}

Extract and return a JSON object with:
1. primary_intent: The main goal (string)
2. secondary_intents: List of related or hidden goals (array of strings)
3. confidence_score: How clear the intent is (0.0 to 1.0)
4. intent_category: Category like "learning", "building", "deciding", "planning", etc.
5. reasoning: Brief explanation of your analysis

Return ONLY valid JSON, no additional text."""

CONSTRAINT_EXTRACTION_PROMPT = """Extract all constraints and context from the user input.

User Input: {user_input}

Extract and return a JSON object with:
{{
  "time_constraint": {{
    "value": "string or null",
    "urgency": "low|medium|high|critical or null"
  }},
  "skill_level": "beginner|intermediate|advanced|expert or null",
  "resources": {{
    "budget": "string or null",
    "tools": ["array of tools mentioned"],
    "team_size": "string or null"
  }},
  "preferences": ["array of stated preferences"],
  "context": "any additional relevant context"
}}

Return ONLY valid JSON. Use null for missing information."""

AMBIGUITY_DETECTION_PROMPT = """Identify ambiguities, missing information, and potential conflicts in the user's request.

User Input: {user_input}
Extracted Intent: {intent_data}
Extracted Constraints: {constraint_data}

Analyze and return a JSON object with:
{{
  "missing_information": ["array of critical missing details"],
  "ambiguous_terms": ["array of unclear or vague terms"],
  "conflicting_constraints": ["array of potential conflicts"],
  "assumptions_needed": ["array of assumptions required to proceed"],
  "clarity_score": 0.0 to 1.0
}}

Return ONLY valid JSON."""

CLARIFICATION_GENERATION_PROMPT = """Generate high-value clarification questions to reduce uncertainty.

User Input: {user_input}
Ambiguity Analysis: {ambiguity_data}

Generate and return a JSON object with:
{{
  "questions": [
    {{
      "question": "the question text",
      "reason": "why this question is important",
      "impact": "high|medium|low"
    }}
  ]
}}

Rules:
- Maximum {max_questions} questions
- Only ask questions that significantly reduce uncertainty
- Prioritize questions by impact
- Make questions specific and actionable

Return ONLY valid JSON."""

ACTION_PLAN_PROMPT = """Generate a detailed, actionable plan based on the user's intent and constraints.

User Input: {user_input}
Intent: {intent_data}
Constraints: {constraint_data}
Clarifications: {clarification_responses}

Generate and return a JSON object with:
{{
  "plan": [
    {{
      "step_number": 1,
      "title": "step title",
      "description": "detailed description",
      "estimated_time": "time estimate",
      "dependencies": ["array of previous step numbers"],
      "resources_needed": ["array of resources"],
      "success_criteria": "how to know this step is complete"
    }}
  ],
  "total_estimated_time": "overall time estimate",
  "critical_path": ["array of step numbers that are critical"],
  "risks": ["array of potential risks"],
  "success_metrics": ["how to measure overall success"]
}}

Return ONLY valid JSON."""

ALTERNATIVE_STRATEGIES_PROMPT = """Generate alternative strategies for different scenarios.

Original Plan: {original_plan}
Constraints: {constraint_data}

Generate and return a JSON object with:
{{
  "alternatives": [
    {{
      "scenario": "if you have less time",
      "strategy": "brief strategy description",
      "key_changes": ["array of main differences"],
      "tradeoffs": "what you gain and lose"
    }},
    {{
      "scenario": "if you are a beginner",
      "strategy": "brief strategy description",
      "key_changes": ["array of main differences"],
      "tradeoffs": "what you gain and lose"
    }},
    {{
      "scenario": "if you want fastest results",
      "strategy": "brief strategy description",
      "key_changes": ["array of main differences"],
      "tradeoffs": "what you gain and lose"
    }}
  ]
}}

Return ONLY valid JSON."""
