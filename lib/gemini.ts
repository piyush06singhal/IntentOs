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
        maxOutputTokens: 4000, // Increased to avoid truncation
        topP: 0.95,
        topK: 40,
        responseMimeType: 'application/json', // Force JSON output
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
  const fullPrompt = `${systemPrompt}

${prompt}

CRITICAL INSTRUCTIONS:
1. Return ONLY valid JSON - no markdown, no explanations, no additional text
2. Ensure all JSON is properly formatted with correct commas and brackets
3. Do not include trailing commas in arrays or objects
4. Escape all special characters in strings
5. Start response with { and end with }

Your response must be parseable by JSON.parse(). Begin your JSON response now:`

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

      // Remove any text before the first {
      const firstBrace = cleanText.indexOf('{')
      if (firstBrace > 0) {
        cleanText = cleanText.substring(firstBrace)
      }

      // Remove any text after the last }
      const lastBrace = cleanText.lastIndexOf('}')
      if (lastBrace > 0 && lastBrace < cleanText.length - 1) {
        cleanText = cleanText.substring(0, lastBrace + 1)
      }

      // Try to parse JSON
      try {
        const parsed = JSON.parse(cleanText)
        return parsed
      } catch (e: any) {
        console.error('JSON Parse Error:', e.message)
        console.error('Problematic JSON:', cleanText.substring(0, 500))
        
        // Try to fix common JSON issues
        try {
          // Remove trailing commas
          let fixed = cleanText.replace(/,(\s*[}\]])/g, '$1')
          // Fix unescaped quotes in strings
          fixed = fixed.replace(/([^\\])"([^"]*)":/g, '$1\\"$2\\":')
          
          const parsed = JSON.parse(fixed)
          console.log('✅ Fixed and parsed JSON')
          return parsed
        } catch (e2) {
          // If still fails, try to extract JSON from the response
          const jsonMatch = cleanText.match(/\{[\s\S]*\}/)
          if (jsonMatch) {
            try {
              return JSON.parse(jsonMatch[0])
            } catch (e3) {
              console.error('All JSON parsing attempts failed')
              throw new Error(`Failed to parse AI response. Error: ${e.message}. Please try again.`)
            }
          }
          throw new Error(`Failed to parse AI response. Error: ${e.message}. Please try again.`)
        }
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
