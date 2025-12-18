'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Target, Zap, Brain, CheckCircle2, ArrowRight } from 'lucide-react'
import Hero from '@/components/Hero'
import InputSection from '@/components/InputSection'
import AnalysisResults from '@/components/AnalysisResults'
import { analyzeIntent } from '@/lib/api'

export default function Home() {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [error, setError] = useState('')

  const handleAnalyze = async () => {
    if (!input.trim()) {
      setError('Please enter your goal')
      return
    }

    setLoading(true)
    setError('')
    
    try {
      const data = await analyzeIntent(input)
      setResults(data)
    } catch (err: any) {
      setError(err.message || 'Failed to analyze. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
      {/* Header */}
      <header className="border-b border-purple-100 bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center">
                <Target className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                  IntentOS
                </h1>
                <p className="text-xs text-gray-500">AI Decision Intelligence</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="hidden md:flex items-center gap-6 text-sm text-gray-600">
                <span className="flex items-center gap-1">
                  <Sparkles className="w-4 h-4" /> AI Powered
                </span>
                <span className="flex items-center gap-1">
                  <Zap className="w-4 h-4" /> Instant Analysis
                </span>
                <span className="flex items-center gap-1">
                  <Brain className="w-4 h-4" /> Smart Planning
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {!results ? (
          <>
            <Hero />
            <InputSection
              input={input}
              setInput={setInput}
              loading={loading}
              error={error}
              onAnalyze={handleAnalyze}
            />
          </>
        ) : (
          <AnalysisResults results={results} onReset={() => {
            setResults(null)
            setInput('')
          }} />
        )}
      </div>

      {/* Footer */}
      <footer className="border-t border-purple-100 bg-white/50 backdrop-blur-sm mt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-sm text-gray-600">
            <p>Built with ❤️ using Next.js, Tailwind CSS, and Google Gemini AI</p>
            <p className="mt-2">© 2024 IntentOS. Transform ambiguity into action.</p>
          </div>
        </div>
      </footer>
    </main>
  )
}
