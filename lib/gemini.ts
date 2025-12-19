import { GoogleGenerativeAI } from '@google/generative-ai'

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '')

// Model fallback chain - try lighter models if quota exceeded
const MODEL_FALLBACK = [
  'gemini-2.0-flash-lite',      // Lightest, lowest quota usage
  'gemini-2.5-flash-lite',      // Light version
  'gemini-2.0-flash',           // Standard
  'gemini-2.5-flash',           // Latest (highest quota)
]

async function tryGenerateWithModel(modelName: string, prompt: string, retryCount = 0): Promise<any> {
  try {
    const model = genAI.getGenerativeModel({ 
      model: modelName,
      generationConfig: {
        temperature: 0.7,
        maxOutputTokens: 2500,
        topP: 0.95,
        topK: 40,
      }
    })

    const result = await model.generateContent(prompt)
    const response = await result.response
    const text = response.text()

    return { success: true, text, model: modelName }
  } catch (error: any) {
    // Check if it's a quota error
    if (error.message?.includes('429') || error.message?.includes('quota')) {
      console.log(`⚠️ Quota exceeded for ${modelName}`)
      return { success: false, error: 'quota', message: error.message }
    }
    
    // Check if it's a rate limit with retry info
    if (error.message?.includes('retry') && retryCount < 2) {
      console.log(`⏳ Rate limited, retrying ${modelName} in 2s...`)
      await new Promise(resolve => setTimeout(resolve, 2000))
      return tryGenerateWithModel(modelName, prompt, retryCount + 1)
    }
    
    return { success: false, error: 'other', message: error.message }
  }
}

export async function generateWithGemini(prompt: string, systemPrompt: string) {
  const fullPrompt = `${systemPrompt}\n\n${prompt}\n\nIMPORTANT: Return ONLY valid JSON, no additional text.`

  // Try models in fallback order
  for (const modelName of MODEL_FALLBACK) {
    console.log(`🤖 Trying model: ${modelName}`)
    const result = await tryGenerateWithModel(modelName, fullPrompt)
    
    if (result.success) {
      console.log(`✅ Success with ${modelName}`)
      let cleanText = result.text.trim()
      
      // Remove markdown code blocks if present
      if (cleanText.startsWith('```json')) {
        cleanText = cleanText.replace(/```json\n?/g, '').replace(/```\n?/g, '')
      } else if (cleanText.startsWith('```')) {
        cleanText = cleanText.replace(/```\n?/g, '')
      }

      // Try to parse JSON
      try {
        return JSON.parse(cleanText)
      } catch (e) {
        // If direct parse fails, try to extract JSON from the response
        const jsonMatch = cleanText.match(/\{[\s\S]*\}/)
        if (jsonMatch) {
          return JSON.parse(jsonMatch[0])
        }
        throw new Error('Failed to parse AI response')
      }
    }
    
    // If quota error, try next model
    if (result.error === 'quota') {
      console.log(`⏭️ Trying next model...`)
      continue
    }
    
    // If other error, throw
    throw new Error(result.message)
  }
  
  // All models failed
  throw new Error('All Gemini models exceeded quota. Please try again later or upgrade your API plan.')
}
