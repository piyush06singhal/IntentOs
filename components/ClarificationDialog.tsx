'use client'

import { motion } from 'framer-motion'
import { HelpCircle, CheckCircle2 } from 'lucide-react'
import { useState } from 'react'

interface ClarificationQuestion {
  question: string
  reason: string
  impact: string
  question_type: string
  suggested_answers: string[]
}

interface ClarificationDialogProps {
  questions: ClarificationQuestion[]
  onSubmit: (answers: { [key: number]: string }) => void
  onSkip: () => void
}

export default function ClarificationDialog({ questions, onSubmit, onSkip }: ClarificationDialogProps) {
  const [answers, setAnswers] = useState<{ [key: number]: string }>({})

  const handleAnswer = (questionIndex: number, answer: string) => {
    setAnswers(prev => ({ ...prev, [questionIndex]: answer }))
  }

  const allAnswered = questions.every((_, index) => answers[index])

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
    >
      <motion.div
        initial={{ y: 20 }}
        animate={{ y: 0 }}
        className="bg-slate-800 rounded-3xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto border border-slate-700"
      >
        {/* Header */}
        <div className="p-8 border-b border-slate-700">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center shadow-lg">
              <HelpCircle className="w-7 h-7 text-white" />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-white">Quick Clarification</h2>
              <p className="text-slate-400">Help us create a better plan for you</p>
            </div>
          </div>
          <p className="text-slate-300">
            We need a bit more information to create the most accurate action plan. 
            Answer these {questions.length} questions or skip to proceed with assumptions.
          </p>
        </div>

        {/* Questions */}
        <div className="p-8 space-y-6">
          {questions.map((q, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-6 bg-slate-900/50 rounded-2xl border border-slate-700"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-white mb-2">
                    {index + 1}. {q.question}
                  </h3>
                  <p className="text-sm text-slate-400 mb-1">
                    <span className="font-semibold">Why this matters:</span> {q.reason}
                  </p>
                  <span className={`inline-block px-3 py-1 rounded-lg text-xs font-bold ${
                    q.impact === 'high' ? 'bg-red-500/20 text-red-300' :
                    q.impact === 'medium' ? 'bg-yellow-500/20 text-yellow-300' :
                    'bg-blue-500/20 text-blue-300'
                  }`}>
                    {q.impact} impact
                  </span>
                </div>
                {answers[index] && (
                  <CheckCircle2 className="w-6 h-6 text-green-400 flex-shrink-0 ml-4" />
                )}
              </div>

              <div className="space-y-2">
                {q.suggested_answers.map((answer, answerIndex) => (
                  <button
                    key={answerIndex}
                    onClick={() => handleAnswer(index, answer)}
                    className={`w-full text-left px-5 py-3 rounded-xl transition-all border-2 ${
                      answers[index] === answer
                        ? 'bg-purple-600 border-purple-500 text-white shadow-lg'
                        : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-purple-500 hover:bg-slate-700'
                    }`}
                  >
                    {answer}
                  </button>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Actions */}
        <div className="p-8 border-t border-slate-700 flex gap-4">
          <button
            onClick={onSkip}
            className="flex-1 px-6 py-4 bg-slate-700 hover:bg-slate-600 text-white rounded-xl font-semibold transition-all"
          >
            Skip & Use Assumptions
          </button>
          <button
            onClick={() => onSubmit(answers)}
            disabled={!allAnswered}
            className="flex-1 px-6 py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl font-semibold hover:shadow-2xl hover:shadow-purple-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {allAnswered ? 'Continue with Answers' : `Answer All Questions (${Object.keys(answers).length}/${questions.length})`}
          </button>
        </div>
      </motion.div>
    </motion.div>
  )
}
