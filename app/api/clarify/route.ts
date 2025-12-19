import { NextResponse } from 'next/server'
import { generateWithGemini } from '@/lib/gemini'
import {
  SYSTEM_ROLE,
  MULTI_INTENT_ANALYSIS_PROMPT,
  CONSTRAINT_EXTRACTION_PROMPT,
  CLARIFICATION_STRATEGY_PROMPT,
} from '@/lib/prompts'

// First stage: Quick analysis to determine if clarification is needed
export async function POST(request: Request) {
  try {
    const { input, sessionHistory = [] } = await request.json()

    if (!input || !input.trim()) {
      return NextResponse.json(
        { error: 'Input is required' },
        { status: 400 }
      )
    }

    console.log('🔍 Stage 1: Quick Intent & Constraint Analysis...')

    // Quick intent analysis
    const intentAnalysis = await generateWithGemini(
      MULTI_INTENT_ANALYSIS_PROMPT(input, sessionHistory),
      SYSTEM_ROLE
    )

    // Quick constraint extraction
    const constraints = await generateWithGemini(
      CONSTRAINT_EXTRACTION_PROMPT(input),
      SYSTEM_ROLE
    )

    // Determine if clarification is needed
    const clarification = await generateWithGemini(
      CLARIFICATION_STRATEGY_PROMPT(input, intentAnalysis, constraints),
      SYSTEM_ROLE
    )

    return NextResponse.json({
      success: true,
      intent: intentAnalysis,
      constraints,
      clarification,
      needs_clarification: clarification.needs_clarification,
    })
  } catch (error: any) {
    console.error('❌ Clarification error:', error)
    
    if (error.message?.includes('quota') || error.message?.includes('429')) {
      return NextResponse.json(
        { 
          success: false,
          error: 'API quota exceeded. Please try again later.',
          errorType: 'quota_exceeded',
        },
        { status: 429 }
      )
    }
    
    return NextResponse.json(
      { 
        success: false,
        error: error.message || 'Failed to analyze',
      },
      { status: 500 }
    )
  }
}
