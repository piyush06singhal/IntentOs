import { NextResponse } from 'next/server'
import { generateWithGemini } from '@/lib/gemini'
import {
  SYSTEM_ROLE,
  MULTI_INTENT_ANALYSIS_PROMPT,
  CLARIFICATION_STRATEGY_PROMPT,
  CONSTRAINT_EXTRACTION_PROMPT,
  MULTI_PLAN_GENERATION_PROMPT,
  VALIDATION_PROMPT,
} from '@/lib/prompts'

// ============================================================================
// INTENTOS ADVANCED REASONING PIPELINE
// Multi-stage AI decision intelligence system
// ============================================================================

export async function POST(request: Request) {
  try {
    const { input, sessionHistory = [] } = await request.json()

    if (!input || !input.trim()) {
      return NextResponse.json(
        { error: 'Input is required' },
        { status: 400 }
      )
    }

    console.log('🚀 Starting IntentOS Advanced Pipeline...')

    // ========================================================================
    // STAGE 1: MULTI-INTENT DECOMPOSITION WITH CONFLICT RESOLUTION
    // ========================================================================
    console.log('📊 Stage 1: Multi-Intent Analysis...')
    const intentAnalysis = await generateWithGemini(
      MULTI_INTENT_ANALYSIS_PROMPT(input, sessionHistory),
      SYSTEM_ROLE
    )

    // ========================================================================
    // STAGE 2: CONSTRAINT EXTRACTION
    // ========================================================================
    console.log('⚙️ Stage 2: Constraint Extraction...')
    const constraints = await generateWithGemini(
      CONSTRAINT_EXTRACTION_PROMPT(input),
      SYSTEM_ROLE
    )

    // ========================================================================
    // STAGE 3: CONFIDENCE-DRIVEN CLARIFICATION ENGINE
    // ========================================================================
    console.log('❓ Stage 3: Clarification Strategy...')
    const clarification = await generateWithGemini(
      CLARIFICATION_STRATEGY_PROMPT(input, intentAnalysis, constraints),
      SYSTEM_ROLE
    )

    // ========================================================================
    // STAGE 4: MULTI-PLAN GENERATION & OPTIMIZATION
    // ========================================================================
    console.log('🎯 Stage 4: Multi-Plan Generation...')
    const planAnalysis = await generateWithGemini(
      MULTI_PLAN_GENERATION_PROMPT(
        input,
        intentAnalysis,
        constraints,
        intentAnalysis.conflicts || []
      ),
      SYSTEM_ROLE
    )

    // ========================================================================
    // STAGE 5: HALLUCINATION & CONTRADICTION GUARDRAIL
    // ========================================================================
    console.log('🛡️ Stage 5: Validation & Guardrails...')
    const validation = await generateWithGemini(
      VALIDATION_PROMPT(input, planAnalysis, constraints),
      SYSTEM_ROLE
    )

    // ========================================================================
    // FINAL OUTPUT ASSEMBLY
    // ========================================================================
    console.log('✅ Pipeline Complete!')

    return NextResponse.json({
      success: true,
      pipeline_version: '2.0-advanced',
      intent: intentAnalysis,
      constraints,
      clarification,
      plans: planAnalysis,
      validation,
      metadata: {
        processing_stages: 5,
        confidence: clarification.overall_confidence,
        needs_clarification: clarification.needs_clarification,
        is_valid: validation.is_valid,
        safe_to_present: validation.safe_to_present,
      },
    })
  } catch (error: any) {
    console.error('❌ Pipeline error:', error)
    
    // Check if it's a quota error
    if (error.message?.includes('quota') || error.message?.includes('429')) {
      return NextResponse.json(
        { 
          success: false,
          error: 'API quota exceeded. The free tier allows 20 requests per day. Please try again later or use a different API key.',
          errorType: 'quota_exceeded',
          stage: 'ai_generation'
        },
        { status: 429 }
      )
    }
    
    return NextResponse.json(
      { 
        success: false,
        error: error.message || 'Failed to analyze',
        stage: 'unknown'
      },
      { status: 500 }
    )
  }
}
