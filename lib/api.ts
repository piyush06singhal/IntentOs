export async function analyzeIntent(userInput: string, sessionHistory: any[] = []) {
  const response = await fetch('/api/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ input: userInput, sessionHistory }),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to analyze')
  }

  return response.json()
}
