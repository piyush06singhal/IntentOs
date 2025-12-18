'use client'

import { motion } from 'framer-motion'
import { Sparkles, Loader2, AlertCircle } from 'lucide-react'

interface InputSectionProps {
  input: string
  setInput: (value: string) => void
  loading: boolean
  error: string
  onAnalyze: () => void
}

export default function InputSection({ input, setInput, loading, error, onAnalyze }: InputSectionProps) {
  const examples = [
    'I want to learn machine learning but don\'t know where to start',
    'I need to build a mobile app for my startup with limited budget',
    'I want to transition from marketing to data science within a year',
  ]

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.7 }}
      className="max-w-4xl mx-auto"
    >
      <div className="bg-white rounded-3xl shadow-2xl p-8 border border-purple-100">
        <label className="block text-lg font-semibold text-gray-800 mb-4">
          💭 What do you want to achieve?
        </label>
        
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your goal... Be as vague or specific as you like!"
          className="w-full h-40 px-6 py-4 text-lg border-2 border-purple-200 rounded-2xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 outline-none transition-all resize-none"
          disabled={loading}
        />

        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl flex items-center gap-2 text-red-700"
          >
            <AlertCircle className="w-5 h-5" />
            <span>{error}</span>
          </motion.div>
        )}

        <div className="mt-6 flex flex-col sm:flex-row gap-4">
          <button
            onClick={onAnalyze}
            disabled={loading || !input.trim()}
            className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                Analyze Goal
              </>
            )}
          </button>
        </div>

        <div className="mt-8">
          <p className="text-sm text-gray-500 mb-3">💡 Try these examples:</p>
          <div className="flex flex-wrap gap-2">
            {examples.map((example, index) => (
              <button
                key={index}
                onClick={() => setInput(example)}
                className="text-sm px-4 py-2 bg-purple-50 hover:bg-purple-100 text-purple-700 rounded-lg transition-colors"
                disabled={loading}
              >
                {example.slice(0, 40)}...
              </button>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  )
}
