import { GoogleGenerativeAI } from '@google/generative-ai'

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '')

export async function generateWithGemini(prompt: string, systemPrompt: string) {
  const model = genAI.getGenerativeModel({ 
    model: 'gemini-2.5-flash',
    generationConfig: {
      temperature: 0.7,
      maxOutputTokens: 2000,
    }
  })

  const fullPrompt = `${systemPrompt}\n\n${prompt}\n\nIMPORTANT: Return ONLY valid JSON, no additional text.`

  const result = await model.generateContent(fullPrompt)
  const response = await result.response
  const text = response.text()

  // Clean the response
  let cleanText = text.trim()
  
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
