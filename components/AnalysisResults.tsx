'use client'

import { motion } from 'framer-motion'
import { Target, Clock, TrendingUp, CheckCircle2, AlertTriangle, Download, RefreshCw } from 'lucide-react'

interface AnalysisResultsProps {
  results: any
  onReset: () => void
}

export default function AnalysisResults({ results, onReset }: AnalysisResultsProps) {
  const { intent, constraints, plan, alternatives } = results

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-6xl mx-auto"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-3xl font-bold text-gray-800">Analysis Complete! 🎉</h2>
          <p className="text-gray-600 mt-2">Here's your personalized action plan</p>
        </div>
        <button
          onClick={onReset}
          className="flex items-center gap-2 px-6 py-3 bg-white border-2 border-purple-200 rounded-xl hover:bg-purple-50 transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          New Analysis
        </button>
      </div>

      {/* Intent Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-2xl p-8 shadow-lg mb-6 border border-purple-100"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
            <Target className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-gray-800">Your Intent</h3>
            <p className="text-sm text-gray-500">What we understood</p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Primary Goal</label>
            <p className="text-lg text-gray-800 mt-1">{intent.primary_intent}</p>
          </div>

          {intent.secondary_intents && intent.secondary_intents.length > 0 && (
            <div>
              <label className="text-sm font-semibold text-gray-600 uppercase tracking-wide">Related Goals</label>
              <ul className="mt-2 space-y-2">
                {intent.secondary_intents.map((item: string, index: number) => (
                  <li key={index} className="flex items-center gap-2 text-gray-700">
                    <CheckCircle2 className="w-4 h-4 text-green-500" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="flex items-center gap-4 pt-4 border-t">
            <div className="flex items-center gap-2">
              <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-green-500 to-emerald-500"
                  style={{ width: `${intent.confidence_score * 100}%` }}
                />
              </div>
              <span className="text-sm font-semibold text-gray-700">
                {Math.round(intent.confidence_score * 100)}% Confidence
              </span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Constraints Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-2xl p-8 shadow-lg mb-6 border border-purple-100"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
            <Clock className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-gray-800">Constraints</h3>
            <p className="text-sm text-gray-500">Your limitations and resources</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {constraints.time_constraint?.value && (
            <div className="p-4 bg-blue-50 rounded-xl">
              <label className="text-sm font-semibold text-blue-700">Time Available</label>
              <p className="text-lg text-gray-800 mt-1">{constraints.time_constraint.value}</p>
            </div>
          )}

          {constraints.skill_level && (
            <div className="p-4 bg-purple-50 rounded-xl">
              <label className="text-sm font-semibold text-purple-700">Skill Level</label>
              <p className="text-lg text-gray-800 mt-1 capitalize">{constraints.skill_level}</p>
            </div>
          )}

          {constraints.resources?.budget && (
            <div className="p-4 bg-green-50 rounded-xl">
              <label className="text-sm font-semibold text-green-700">Budget</label>
              <p className="text-lg text-gray-800 mt-1">{constraints.resources.budget}</p>
            </div>
          )}

          {constraints.resources?.tools && constraints.resources.tools.length > 0 && (
            <div className="p-4 bg-orange-50 rounded-xl">
              <label className="text-sm font-semibold text-orange-700">Available Tools</label>
              <div className="flex flex-wrap gap-2 mt-2">
                {constraints.resources.tools.map((tool: string, index: number) => (
                  <span key={index} className="px-3 py-1 bg-white rounded-lg text-sm text-gray-700">
                    {tool}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </motion.div>

      {/* Action Plan */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white rounded-2xl p-8 shadow-lg mb-6 border border-purple-100"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
            <TrendingUp className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-gray-800">Action Plan</h3>
            <p className="text-sm text-gray-500">Step-by-step roadmap to success</p>
          </div>
        </div>

        <div className="space-y-4">
          {plan.plan && plan.plan.map((step: any, index: number) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 + index * 0.1 }}
              className="p-6 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border-l-4 border-purple-500 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 rounded-full bg-purple-500 text-white flex items-center justify-center font-bold flex-shrink-0">
                  {step.step_number}
                </div>
                <div className="flex-1">
                  <h4 className="text-lg font-semibold text-gray-800 mb-2">{step.title}</h4>
                  <p className="text-gray-700 mb-3">{step.description}</p>
                  
                  <div className="flex flex-wrap gap-4 text-sm">
                    {step.estimated_time && (
                      <span className="flex items-center gap-1 text-gray-600">
                        <Clock className="w-4 h-4" />
                        {step.estimated_time}
                      </span>
                    )}
                    {step.resources_needed && step.resources_needed.length > 0 && (
                      <div className="flex items-center gap-2">
                        {step.resources_needed.map((resource: string, i: number) => (
                          <span key={i} className="px-2 py-1 bg-white rounded text-xs">
                            {resource}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>

                  {step.success_criteria && (
                    <div className="mt-3 p-3 bg-green-50 rounded-lg">
                      <p className="text-sm text-green-800">
                        <CheckCircle2 className="w-4 h-4 inline mr-1" />
                        Success: {step.success_criteria}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {plan.risks && plan.risks.length > 0 && (
          <div className="mt-6 p-6 bg-yellow-50 rounded-xl border border-yellow-200">
            <h4 className="font-semibold text-yellow-800 mb-3 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              Potential Risks
            </h4>
            <ul className="space-y-2">
              {plan.risks.map((risk: string, index: number) => (
                <li key={index} className="text-yellow-800 text-sm">• {risk}</li>
              ))}
            </ul>
          </div>
        )}
      </motion.div>

      {/* Download Button */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="flex justify-center"
      >
        <button
          onClick={() => {
            const dataStr = JSON.stringify(results, null, 2)
            const dataBlob = new Blob([dataStr], { type: 'application/json' })
            const url = URL.createObjectURL(dataBlob)
            const link = document.createElement('a')
            link.href = url
            link.download = 'intentos-plan.json'
            link.click()
          }}
          className="flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold hover:shadow-2xl hover:scale-105 transition-all"
        >
          <Download className="w-5 h-5" />
          Download Plan
        </button>
      </motion.div>
    </motion.div>
  )
}
