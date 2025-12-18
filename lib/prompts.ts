export const SYSTEM_ROLE = `You are IntentOS, an AI decision intelligence system designed to understand user intent and generate actionable plans.

Core Principles:
- Never assume missing data
- Prefer asking clarification over hallucinating
- Think like a consultant, not a chatbot
- Prioritize usefulness over verbosity
- Always produce structured, machine-readable output

Your role is to be precise, analytical, and helpful.`

export const INTENT_EXTRACTION_PROMPT = (userInput: string) => `
Analyze the following user input and extract structured intent information.

User Input: ${userInput}

Extract and return a JSON object with:
1. primary_intent: The main goal (string)
2. secondary_intents: List of related or hidden goals (array of strings)
3. confidence_score: How clear the intent is (0.0 to 1.0)
4. intent_category: Category like "learning", "building", "deciding", "planning", etc.
5. reasoning: Brief explanation of your analysis

Return ONLY valid JSON, no additional text.`

export const CONSTRAINT_EXTRACTION_PROMPT = (userInput: string) => `
Extract all constraints and context from the user input.

User Input: ${userInput}

Extract and return a JSON object with:
{
  "time_constraint": {
    "value": "string or null",
    "urgency": "low|medium|high|critical or null"
  },
  "skill_level": "beginner|intermediate|advanced|expert or null",
  "resources": {
    "budget": "string or null",
    "tools": ["array of tools mentioned"],
    "team_size": "string or null"
  },
  "preferences": ["array of stated preferences"],
  "context": "any additional relevant context"
}

Return ONLY valid JSON. Use null for missing information.`

export const ACTION_PLAN_PROMPT = (userInput: string, intent: any, constraints: any) => `
Generate a detailed, actionable plan based on the user's intent and constraints.

User Input: ${userInput}
Intent: ${JSON.stringify(intent)}
Constraints: ${JSON.stringify(constraints)}

Generate and return a JSON object with:
{
  "plan": [
    {
      "step_number": 1,
      "title": "step title",
      "description": "detailed description",
      "estimated_time": "time estimate",
      "dependencies": ["array of previous step numbers"],
      "resources_needed": ["array of resources"],
      "success_criteria": "how to know this step is complete"
    }
  ],
  "total_estimated_time": "overall time estimate",
  "critical_path": ["array of step numbers that are critical"],
  "risks": ["array of potential risks"],
  "success_metrics": ["how to measure overall success"]
}

Return ONLY valid JSON.`
