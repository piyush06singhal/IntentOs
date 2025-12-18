import { GoogleGenerativeAI } from '@google/generative-ai'

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '')

export async function generateWithGemini(prompt: string, systemPrompt: string) {
  const model = genAI.getGenerativeModel({ model: 'gemini-pro' })

  const fullPrompt = `${systemPrompt}\n\n${prompt}\n\nIMPORTANT: Return ONLY valid JSON, no additional text.`

  const result = await model.generateContent(fullPrompt)
  const response = await result.response
  const text = response.text()

  // Try to parse JSON
  try {
    return JSON.parse(text)
  } catch (e) {
    // If direct parse fails, try to extract JSON from the response
    const jsonMatch = text.match(/\{[\s\S]*\}/)
    if (jsonMatch) {
      return JSON.parse(jsonMatch[0])
    }
    throw new Error('Failed to parse AI response')
  }
}
