import { NextResponse } from 'next/server'
import { generateWithGemini } from '@/lib/gemini'
import {
  SYSTEM_ROLE,
  INTENT_EXTRACTION_PROMPT,
  CONSTRAINT_EXTRACTION_PROMPT,
  ACTION_PLAN_PROMPT,
} from '@/lib/prompts'

export async function POST(request: Request) {
  try {
    const { input } = await request.json()

    if (!input || !input.trim()) {
      return NextResponse.json(
        { error: 'Input is required' },
        { status: 400 }
      )
    }

    // Step 1: Extract Intent
    const intent = await generateWithGemini(
      INTENT_EXTRACTION_PROMPT(input),
      SYSTEM_ROLE
    )

    // Step 2: Extract Constraints
    const constraints = await generateWithGemini(
      CONSTRAINT_EXTRACTION_PROMPT(input),
      SYSTEM_ROLE
    )

    // Step 3: Generate Action Plan
    const plan = await generateWithGemini(
      ACTION_PLAN_PROMPT(input, intent, constraints),
      SYSTEM_ROLE
    )

    return NextResponse.json({
      intent,
      constraints,
      plan,
      alternatives: [],
    })
  } catch (error: any) {
    console.error('Analysis error:', error)
    return NextResponse.json(
      { error: error.message || 'Failed to analyze' },
      { status: 500 }
    )
  }
}
