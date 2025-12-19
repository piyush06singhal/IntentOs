'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Target, Sparkles, Loader2, CheckCircle2, Clock, TrendingUp, Download, 
  RefreshCw, AlertCircle, Lightbulb, Zap, Brain, AlertTriangle, 
  Shield, GitBranch, Activity, Award, ChevronDown, ChevronUp, History
} from 'lucide-react'
import { analyzeIntent } from '@/lib/api'
import ClarificationDialog from '@/components/ClarificationDialog'
import VisualizationCharts from '@/components/VisualizationCharts'

export default function Home() {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingStage, setLoadingStage] = useState('')
  const [results, setResults] = useState<any>(null)
  const [error, setError] = useState('')
  const [sessionHistory, setSessionHistory] = useState<any[]>([])
  const [showClarification, setShowClarification] = useState(false)
  const [clarificationData, setClarificationData] = useState<any>(null)
  const [userAnswers, setUserAnswers] = useState<any>(null)
  const [expandedSections, setExpandedSections] = useState<{[key: string]: boolean}>({
    conflicts: true,
    clarification: true,
    alternatives: false,
    validation: false,
  })

  useEffect(() => {
    const saved = localStorage.getItem('intentos_history')
    if (saved) {
      try {
        setSessionHistory(JSON.parse(saved))
      } catch (e) {
        console.error('Failed to load history')
      }
    }
  }, [])

  const proceedWithFullAnalysis = async (answers?: any) => {
    setLoading(true)
    setLoadingStage('Generating detailed action plans...')
    setError('')
    
    try {
      const data = await analyzeIntent(input, sessionHistory, answers)
      setResults(data)
      
      const newHistory = [...sessionHistory, { input, timestamp: Date.now(), intent: data.intent }]
      setSessionHistory(newHistory.slice(-5))
      localStorage.setItem('intentos_history', JSON.stringify(newHistory.slice(-5)))
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to analyze. Please try again.'
      
      if (errorMessage.includes('quota') || errorMessage.includes('429')) {
        setError('⚠️ API Quota Exceeded: The free tier allows 20 requests per day. Please wait 24 hours or use a different API key.')
      } else {
        setError(errorMessage)
      }
    } finally {
      setLoading(false)
      setLoadingStage('')
    }
  }

  const handleAnalyze = async () => {
    if (!input.trim()) {
      setError('Please enter your goal')
      return
    }

    setLoading(true)
    setLoadingStage('Analyzing your goal...')
    setError('')
    
    try {
      // Stage 1: Quick clarification check
      const clarifyResponse = await fetch('/api/clarify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input, sessionHistory }),
      })

      const clarifyData = await clarifyResponse.json()

      if (!clarifyData.success) {
        throw new Error(clarifyData.error)
      }

      // Check if clarification is needed
      if (clarifyData.needs_clarification && clarifyData.clarification.clarification_questions?.length > 0) {
        setLoading(false)
        setShowClarification(true)
        setClarificationData(clarifyData)
      } else {
        // Proceed directly to full analysis
        setLoadingStage('No clarification needed, proceeding with analysis...')
        await proceedWithFullAnalysis()
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to analyze. Please try again.'
      
      if (errorMessage.includes('quota') || errorMessage.includes('429')) {
        setError('⚠️ API Quota Exceeded: Please wait 24 hours or use a different API key.')
      } else {
        setError(errorMessage)
      }
      setLoading(false)
      setLoadingStage('')
    }
  }

  const handleClarificationSubmit = (answers: any) => {
    setShowClarification(false)
    setUserAnswers(answers)
    proceedWithFullAnalysis(answers)
  }

  const handleClarificationSkip = () => {
    setShowClarification(false)
    proceedWithFullAnalysis()
  }

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }))
  }

  const examples = [
    'I want to learn machine learning but don\'t know where to start and only have 10 hours per week',
    'I need to build a mobile app for my startup with limited budget and no coding experience',
    'I want to transition from marketing to data science within a year while working full-time',
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      {/* Header */}
      <header className="relative bg-slate-900/80 backdrop-blur-xl border-b border-slate-700/50 sticky top-0 z-50 shadow-2xl">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl blur-lg opacity-75 animate-pulse" />
                <div className="relative w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-600 via-blue-600 to-purple-600 flex items-center justify-center shadow-2xl">
                  <Target className="w-8 h-8 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-3xl font-black bg-gradient-to-r from-purple-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                  IntentOS
                </h1>
                <p className="text-xs text-slate-400 font-medium tracking-wide">AI Decision Intelligence v2.0</p>
              </div>
            </div>
            <div className="hidden md:flex items-center gap-6">
              <div className="flex items-center gap-2 px-4 py-2 bg-slate-800/50 rounded-xl border border-slate-700/50">
                <Brain className="w-4 h-4 text-purple-400" />
                <span className="text-sm text-slate-300 font-medium">5 AI Features</span>
              </div>
              {sessionHistory.length > 0 && (
                <div className="flex items-center gap-2 px-4 py-2 bg-slate-800/50 rounded-xl border border-slate-700/50">
                  <History className="w-4 h-4 text-blue-400" />
                  <span className="text-sm text-slate-300 font-medium">{sessionHistory.length} Sessions</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="relative container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <AnimatePresence mode="wait">
          {!results ? (
            <motion.div
              key="input"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {/* Hero Section */}
              <div className="text-center mb-16">
                <motion.div
                  initial={{ scale: 0, rotate: -180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{ type: 'spring', duration: 0.8 }}
                  className="inline-block mb-8"
                >
                  <div className="relative">
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-blue-600 rounded-3xl blur-2xl opacity-50 animate-pulse" />
                    <div className="relative w-28 h-28 rounded-3xl bg-gradient-to-br from-purple-600 via-blue-600 to-purple-600 flex items-center justify-center shadow-2xl">
                      <Target className="w-14 h-14 text-white" />
                    </div>
                  </div>
                </motion.div>

                <motion.h1
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="text-6xl md:text-8xl font-black mb-6 leading-tight"
                >
                  <span className="bg-gradient-to-r from-purple-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                    Transform Ambiguity
                  </span>
                  <br />
                  <span className="text-white">into Action</span>
                </motion.h1>

                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  className="text-xl text-slate-300 max-w-3xl mx-auto mb-12 leading-relaxed"
                >
                  IntentOS uses advanced AI to understand your goals, detect conflicts, 
                  ask intelligent questions, and generate optimized action plans.
                </motion.p>

                {/* Feature Grid */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="grid grid-cols-1 md:grid-cols-5 gap-4 max-w-6xl mx-auto mb-16"
                >
                  {[
                    { icon: GitBranch, title: 'Multi-Intent', desc: 'Detects conflicts', color: 'from-purple-500 to-pink-500' },
                    { icon: Lightbulb, title: 'Smart Questions', desc: 'Only when needed', color: 'from-yellow-500 to-orange-500' },
                    { icon: Activity, title: 'Multi-Plan', desc: 'Optimized options', color: 'from-blue-500 to-cyan-500' },
                    { icon: History, title: 'Memory', desc: 'Tracks evolution', color: 'from-green-500 to-emerald-500' },
                    { icon: Shield, title: 'Guardrails', desc: 'Validates output', color: 'from-red-500 to-rose-500' },
                  ].map((feature, index) => (
                    <motion.div
                      key={feature.title}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.5 + index * 0.1 }}
                      whileHover={{ scale: 1.05, y: -5 }}
                      className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-6 border border-slate-700/50 hover:border-slate-600 transition-all shadow-xl"
                    >
                      <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-3 shadow-lg`}>
                        <feature.icon className="w-6 h-6 text-white" />
                      </div>
                      <h3 className="text-sm font-bold text-white mb-1">{feature.title}</h3>
                      <p className="text-xs text-slate-400">{feature.desc}</p>
                    </motion.div>
                  ))}
                </motion.div>
              </div>
              {/* Input Section */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8 }}
                className="max-w-5xl mx-auto"
              >
                <div className="bg-slate-800/50 backdrop-blur-xl rounded-3xl shadow-2xl p-8 md:p-12 border border-slate-700/50">
                  <label className="block text-2xl font-bold text-white mb-2 flex items-center gap-3">
                    <Sparkles className="w-7 h-7 text-purple-400" />
                    What do you want to achieve?
                  </label>
                  <p className="text-slate-400 mb-6">
                    Be as vague or specific as you like. IntentOS will understand, clarify, and plan.
                  </p>
                  
                  <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Example: I want to learn machine learning but I'm not sure where to start and I only have 10 hours per week..."
                    className="w-full h-48 px-6 py-4 text-lg bg-slate-900/50 border-2 border-slate-700 text-white placeholder-slate-500 rounded-2xl focus:border-purple-500 focus:ring-4 focus:ring-purple-500/20 outline-none transition-all resize-none"
                    disabled={loading}
                  />

                  {error && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="mt-4 p-4 bg-red-500/10 border-l-4 border-red-500 rounded-xl flex items-center gap-3 text-red-400"
                    >
                      <AlertCircle className="w-5 h-5 flex-shrink-0" />
                      <span>{error}</span>
                    </motion.div>
                  )}

                  <div className="mt-8">
                    <button
                      onClick={handleAnalyze}
                      disabled={loading || !input.trim()}
                      className="w-full bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 text-white px-8 py-5 rounded-2xl font-bold text-lg hover:shadow-2xl hover:shadow-purple-500/50 hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-3"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="w-6 h-6 animate-spin" />
                          {loadingStage || 'Processing...'}
                        </>
                      ) : (
                        <>
                          <Brain className="w-6 h-6" />
                          Analyze with IntentOS
                        </>
                      )}
                    </button>
                  </div>

                  <div className="mt-8">
                    <p className="text-sm font-semibold text-slate-400 mb-4 flex items-center gap-2">
                      <Lightbulb className="w-4 h-4" />
                      Try these examples:
                    </p>
                    <div className="grid grid-cols-1 gap-3">
                      {examples.map((example, index) => (
                        <button
                          key={index}
                          onClick={() => setInput(example)}
                          className="text-left px-5 py-3 bg-slate-900/50 hover:bg-slate-900/80 text-slate-300 rounded-xl transition-all border border-slate-700/50 hover:border-purple-500/50 hover:shadow-lg text-sm"
                          disabled={loading}
                        >
                          {example}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          ) : (
            <motion.div
              key="results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="max-w-7xl mx-auto"
            >
              {/* Results Header */}
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h2 className="text-4xl font-black text-white mb-2 flex items-center gap-3">
                    <Award className="w-10 h-10 text-purple-400" />
                    Analysis Complete
                  </h2>
                  <p className="text-slate-400">Advanced 5-stage pipeline processing complete</p>
                </div>
                <button
                  onClick={() => {
                    setResults(null)
                    setInput('')
                  }}
                  className="flex items-center gap-2 px-6 py-3 bg-slate-800/50 border-2 border-slate-700 rounded-xl hover:bg-slate-700/50 transition-all font-semibold text-white shadow-lg"
                >
                  <RefreshCw className="w-5 h-5" />
                  New Analysis
                </button>
              </div>

              {/* Pipeline Status */}
              {results.metadata && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-6 shadow-xl mb-6 border border-slate-700/50"
                >
                  <div className="flex items-center justify-between flex-wrap gap-4">
                    <div className="flex items-center gap-3">
                      <Activity className="w-6 h-6 text-green-400" />
                      <div>
                        <p className="text-sm text-slate-400">Pipeline Status</p>
                        <p className="text-lg font-bold text-white">{results.metadata.processing_stages} Stages Complete</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${results.metadata.safe_to_present ? 'bg-green-400' : 'bg-yellow-400'} animate-pulse`} />
                      <span className="text-sm text-slate-300">
                        {results.metadata.safe_to_present ? 'Validated & Safe' : 'Needs Review'}
                      </span>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="w-32 h-2 bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-purple-500 to-blue-500"
                          style={{ width: `${results.metadata.confidence * 100}%` }}
                        />
                      </div>
                      <span className="text-sm font-bold text-white">
                        {Math.round(results.metadata.confidence * 100)}% Confidence
                      </span>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Visualization Charts */}
              {results.intent && results.constraints && results.plans && (
                <VisualizationCharts 
                  intent={results.intent}
                  constraints={results.constraints}
                  plans={results.plans}
                />
              )}

              {/* FEATURE 1: Multi-Intent with Conflicts */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="bg-slate-800/50 backdrop-blur-xl rounded-3xl p-8 shadow-xl mb-6 border border-slate-700/50"
              >
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-4">
                    <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
                      <GitBranch className="w-7 h-7 text-white" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-white">Multi-Intent Analysis</h3>
                      <p className="text-sm text-slate-400">Primary, secondary, and hidden goals detected</p>
                    </div>
                  </div>
                  <div className="px-4 py-2 bg-purple-500/20 rounded-xl border border-purple-500/30">
                    <span className="text-sm font-bold text-purple-300">Feature #1</span>
                  </div>
                </div>

                {/* Primary Intent */}
                <div className="p-6 bg-gradient-to-r from-purple-900/30 to-pink-900/30 rounded-2xl mb-4 border border-purple-500/30">
                  <label className="text-xs font-bold text-purple-300 uppercase tracking-wide">Primary Goal</label>
                  <p className="text-xl text-white mt-2 font-medium">{results.intent.primary_intent.goal}</p>
                  <div className="flex items-center gap-4 mt-3">
                    <span className="px-3 py-1 bg-purple-500/20 rounded-lg text-sm text-purple-300 font-medium">
                      {results.intent.primary_intent.category}
                    </span>
                    <span className="text-sm text-slate-400">
                      Clarity: {Math.round(results.intent.primary_intent.clarity_score * 100)}%
                    </span>
                  </div>
                </div>

                {/* Secondary Intents */}
                {results.intent.secondary_intents && results.intent.secondary_intents.length > 0 && (
                  <div className="mb-4">
                    <label className="text-sm font-bold text-slate-300 uppercase tracking-wide mb-3 block">Secondary Goals</label>
                    <div className="grid md:grid-cols-2 gap-3">
                      {results.intent.secondary_intents.map((item: any, index: number) => (
                        <div key={index} className="p-4 bg-slate-900/50 rounded-xl border border-slate-700/50">
                          <p className="text-white font-medium mb-2">{item.goal}</p>
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-1 bg-blue-500/20 rounded text-xs text-blue-300">{item.relationship}</span>
                            <span className="px-2 py-1 bg-yellow-500/20 rounded text-xs text-yellow-300">{item.priority}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Hidden Intents */}
                {results.intent.hidden_intents && results.intent.hidden_intents.length > 0 && (
                  <div className="mb-4">
                    <label className="text-sm font-bold text-slate-300 uppercase tracking-wide mb-3 block flex items-center gap-2">
                      <Lightbulb className="w-4 h-4 text-yellow-400" />
                      Hidden Intents (AI Inferred)
                    </label>
                    <div className="space-y-3">
                      {results.intent.hidden_intents.map((item: any, index: number) => (
                        <div key={index} className="p-4 bg-yellow-900/20 rounded-xl border border-yellow-500/30">
                          <p className="text-white font-medium mb-2">{item.inferred_goal}</p>
                          <p className="text-sm text-slate-400 mb-2">{item.reasoning}</p>
                          <span className="text-xs text-yellow-300">
                            Confidence: {Math.round(item.confidence * 100)}%
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Conflicts */}
                {results.intent.conflicts && results.intent.conflicts.length > 0 && (
                  <div>
                    <button
                      onClick={() => toggleSection('conflicts')}
                      className="w-full flex items-center justify-between p-4 bg-red-900/20 rounded-xl border border-red-500/30 hover:bg-red-900/30 transition-all mb-2"
                    >
                      <div className="flex items-center gap-3">
                        <AlertTriangle className="w-5 h-5 text-red-400" />
                        <span className="font-bold text-red-300">Detected Conflicts ({results.intent.conflicts.length})</span>
                      </div>
                      {expandedSections.conflicts ? <ChevronUp className="w-5 h-5 text-red-400" /> : <ChevronDown className="w-5 h-5 text-red-400" />}
                    </button>
                    {expandedSections.conflicts && (
                      <div className="space-y-3 mt-3">
                        {results.intent.conflicts.map((conflict: any, index: number) => (
                          <div key={index} className="p-4 bg-slate-900/50 rounded-xl border-l-4 border-red-500">
                            <div className="flex items-start justify-between mb-2">
                              <p className="text-white font-medium">{conflict.description}</p>
                              <span className={`px-2 py-1 rounded text-xs ${
                                conflict.severity === 'critical' ? 'bg-red-500/20 text-red-300' :
                                conflict.severity === 'high' ? 'bg-orange-500/20 text-orange-300' :
                                'bg-yellow-500/20 text-yellow-300'
                              }`}>
                                {conflict.severity}
                              </span>
                            </div>
                            <p className="text-sm text-green-400 flex items-center gap-2">
                              <CheckCircle2 className="w-4 h-4" />
                              Resolution: {conflict.resolution_strategy}
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </motion.div>
              {/* FEATURE 2: Clarification Engine */}
              {results.clarification && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="bg-slate-800/50 backdrop-blur-xl rounded-3xl p-8 shadow-xl mb-6 border border-slate-700/50"
                >
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-4">
                      <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center shadow-lg">
                        <Lightbulb className="w-7 h-7 text-white" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-white">Clarification Engine</h3>
                        <p className="text-sm text-slate-400">Intelligent questions only when needed</p>
                      </div>
                    </div>
                    <div className="px-4 py-2 bg-yellow-500/20 rounded-xl border border-yellow-500/30">
                      <span className="text-sm font-bold text-yellow-300">Feature #2</span>
                    </div>
                  </div>

                  <div className="p-6 bg-gradient-to-r from-yellow-900/20 to-orange-900/20 rounded-2xl mb-4 border border-yellow-500/30">
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-sm font-bold text-yellow-300">Needs Clarification?</span>
                      <span className={`px-4 py-2 rounded-xl font-bold ${
                        results.clarification.needs_clarification 
                          ? 'bg-yellow-500/20 text-yellow-300' 
                          : 'bg-green-500/20 text-green-300'
                      }`}>
                        {results.clarification.needs_clarification ? 'Yes' : 'No - Can Proceed'}
                      </span>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-sm text-slate-400">Overall Confidence:</span>
                      <div className="flex-1 max-w-xs h-3 bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-yellow-500 to-green-500"
                          style={{ width: `${results.clarification.overall_confidence * 100}%` }}
                        />
                      </div>
                      <span className="text-lg font-bold text-white">
                        {Math.round(results.clarification.overall_confidence * 100)}%
                      </span>
                    </div>
                  </div>

                  {results.clarification.clarification_questions && results.clarification.clarification_questions.length > 0 && (
                    <div>
                      <button
                        onClick={() => toggleSection('clarification')}
                        className="w-full flex items-center justify-between p-4 bg-yellow-900/20 rounded-xl border border-yellow-500/30 hover:bg-yellow-900/30 transition-all mb-3"
                      >
                        <span className="font-bold text-yellow-300">
                          Clarification Questions ({results.clarification.clarification_questions.length})
                        </span>
                        {expandedSections.clarification ? <ChevronUp className="w-5 h-5 text-yellow-400" /> : <ChevronDown className="w-5 h-5 text-yellow-400" />}
                      </button>
                      {expandedSections.clarification && (
                        <div className="space-y-4">
                          {results.clarification.clarification_questions.map((q: any, index: number) => (
                            <div key={index} className="p-5 bg-slate-900/50 rounded-xl border border-slate-700/50">
                              <div className="flex items-start justify-between mb-3">
                                <p className="text-white font-medium flex-1">{q.question}</p>
                                <span className={`px-3 py-1 rounded-lg text-xs font-bold ml-3 ${
                                  q.impact === 'high' ? 'bg-red-500/20 text-red-300' :
                                  q.impact === 'medium' ? 'bg-yellow-500/20 text-yellow-300' :
                                  'bg-blue-500/20 text-blue-300'
                                }`}>
                                  {q.impact} impact
                                </span>
                              </div>
                              <p className="text-sm text-slate-400 mb-3">{q.reason}</p>
                              {q.suggested_answers && q.suggested_answers.length > 0 && (
                                <div className="flex flex-wrap gap-2">
                                  {q.suggested_answers.map((answer: string, i: number) => (
                                    <span key={i} className="px-3 py-1 bg-slate-800 rounded-lg text-sm text-slate-300 border border-slate-700">
                                      {answer}
                                    </span>
                                  ))}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {results.clarification.can_proceed_without_clarification && (
                    <div className="mt-4 p-4 bg-green-900/20 rounded-xl border border-green-500/30">
                      <p className="text-sm text-green-300 font-medium mb-2">✓ Can proceed with assumptions:</p>
                      <ul className="space-y-1">
                        {results.clarification.assumptions_if_proceeding?.map((assumption: string, index: number) => (
                          <li key={index} className="text-sm text-slate-400">• {assumption}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </motion.div>
              )}
              {/* Constraints */}
              {results.constraints && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                  className="bg-slate-800/50 backdrop-blur-xl rounded-3xl p-8 shadow-xl mb-6 border border-slate-700/50"
                >
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center shadow-lg">
                      <Clock className="w-7 h-7 text-white" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-white">Constraints & Resources</h3>
                      <p className="text-sm text-slate-400">Your limitations and available resources</p>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4">
                    {results.constraints.time_constraint?.value && (
                      <div className="p-5 bg-blue-900/20 rounded-2xl border border-blue-500/30">
                        <label className="text-xs font-bold text-blue-300 uppercase tracking-wide">Time Available</label>
                        <p className="text-lg text-white mt-2 font-semibold">{results.constraints.time_constraint.value}</p>
                        <span className="text-sm text-slate-400">Urgency: {results.constraints.time_constraint.urgency}</span>
                      </div>
                    )}

                    {results.constraints.skill_level?.current && (
                      <div className="p-5 bg-purple-900/20 rounded-2xl border border-purple-500/30">
                        <label className="text-xs font-bold text-purple-300 uppercase tracking-wide">Skill Level</label>
                        <p className="text-lg text-white mt-2 font-semibold capitalize">{results.constraints.skill_level.current}</p>
                        {results.constraints.skill_level.target && (
                          <span className="text-sm text-slate-400">Target: {results.constraints.skill_level.target}</span>
                        )}
                      </div>
                    )}

                    {results.constraints.resources?.budget && (
                      <div className="p-5 bg-green-900/20 rounded-2xl border border-green-500/30">
                        <label className="text-xs font-bold text-green-300 uppercase tracking-wide">Budget</label>
                        <p className="text-lg text-white mt-2 font-semibold">{results.constraints.resources.budget}</p>
                      </div>
                    )}

                    {results.constraints.preferences?.priorities && results.constraints.preferences.priorities.length > 0 && (
                      <div className="p-5 bg-orange-900/20 rounded-2xl border border-orange-500/30">
                        <label className="text-xs font-bold text-orange-300 uppercase tracking-wide mb-3 block">Priorities</label>
                        <div className="flex flex-wrap gap-2">
                          {results.constraints.preferences.priorities.map((priority: string, index: number) => (
                            <span key={index} className="px-3 py-1 bg-slate-800 rounded-lg text-sm font-medium text-white">
                              {priority}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {results.constraints.blockers && results.constraints.blockers.length > 0 && (
                    <div className="mt-4 p-5 bg-red-900/20 rounded-2xl border border-red-500/30">
                      <label className="text-sm font-bold text-red-300 uppercase tracking-wide mb-3 block flex items-center gap-2">
                        <AlertTriangle className="w-4 h-4" />
                        Potential Blockers
                      </label>
                      <div className="space-y-2">
                        {results.constraints.blockers.map((blocker: any, index: number) => (
                          <div key={index} className="flex items-start gap-3">
                            <span className={`px-2 py-1 rounded text-xs font-bold ${
                              blocker.severity === 'critical' ? 'bg-red-500/30 text-red-300' :
                              blocker.severity === 'high' ? 'bg-orange-500/30 text-orange-300' :
                              'bg-yellow-500/30 text-yellow-300'
                            }`}>
                              {blocker.severity}
                            </span>
                            <p className="text-sm text-slate-300 flex-1">{blocker.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </motion.div>
              )}
              {/* FEATURE 3: Multi-Plan Optimization */}
              {results.plans && results.plans.candidate_plans && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="bg-slate-800/50 backdrop-blur-xl rounded-3xl p-8 shadow-xl mb-6 border border-slate-700/50"
                >
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-4">
                      <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center shadow-lg">
                        <Activity className="w-7 h-7 text-white" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-white">Multi-Plan Optimization</h3>
                        <p className="text-sm text-slate-400">Multiple strategies optimized for different priorities</p>
                      </div>
                    </div>
                    <div className="px-4 py-2 bg-green-500/20 rounded-xl border border-green-500/30">
                      <span className="text-sm font-bold text-green-300">Feature #3</span>
                    </div>
                  </div>

                  {/* Recommended Plan Badge */}
                  <div className="p-4 bg-gradient-to-r from-green-900/30 to-emerald-900/30 rounded-2xl mb-6 border border-green-500/30">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-green-300 font-bold uppercase tracking-wide">Recommended Plan</p>
                        <p className="text-xl text-white font-bold capitalize mt-1">{results.plans.recommended_plan?.replace('_', ' ')}</p>
                      </div>
                      <Award className="w-10 h-10 text-green-400" />
                    </div>
                    <p className="text-sm text-slate-300 mt-3">{results.plans.recommendation_reasoning}</p>
                  </div>

                  {/* Plan Tabs */}
                  <div className="space-y-4">
                    {results.plans.candidate_plans.map((plan: any, planIndex: number) => {
                      const isRecommended = plan.plan_id === results.plans.recommended_plan
                      return (
                        <div
                          key={planIndex}
                          className={`p-6 rounded-2xl border-2 ${
                            isRecommended 
                              ? 'bg-green-900/20 border-green-500/50' 
                              : 'bg-slate-900/50 border-slate-700/50'
                          }`}
                        >
                          <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-3">
                              <h4 className="text-xl font-bold text-white capitalize">{plan.plan_id.replace('_', ' ')}</h4>
                              {isRecommended && (
                                <span className="px-3 py-1 bg-green-500/20 rounded-lg text-xs font-bold text-green-300">
                                  ⭐ RECOMMENDED
                                </span>
                              )}
                            </div>
                            <span className="text-sm text-slate-400">Focus: {plan.optimization_focus}</span>
                          </div>

                          {/* Constraint Satisfaction Scores */}
                          <div className="grid grid-cols-3 gap-3 mb-4">
                            {Object.entries(plan.constraint_satisfaction || {}).map(([key, value]: [string, any]) => (
                              <div key={key} className="p-3 bg-slate-800/50 rounded-xl">
                                <p className="text-xs text-slate-400 capitalize mb-1">{key}</p>
                                <div className="flex items-center gap-2">
                                  <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                                    <div
                                      className={`h-full ${
                                        value > 0.7 ? 'bg-green-500' : value > 0.4 ? 'bg-yellow-500' : 'bg-red-500'
                                      }`}
                                      style={{ width: `${value * 100}%` }}
                                    />
                                  </div>
                                  <span className="text-xs font-bold text-white">{Math.round(value * 100)}%</span>
                                </div>
                              </div>
                            ))}
                          </div>

                          {/* Steps */}
                          <div className="space-y-3">
                            {plan.plan.map((step: any, stepIndex: number) => (
                              <div
                                key={stepIndex}
                                className="p-4 bg-slate-900/50 rounded-xl border-l-4 border-purple-500 hover:bg-slate-900/70 transition-all"
                              >
                                <div className="flex items-start gap-4">
                                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-600 to-blue-600 text-white flex items-center justify-center font-bold flex-shrink-0">
                                    {step.step_number}
                                  </div>
                                  <div className="flex-1">
                                    <h5 className="text-lg font-bold text-white mb-2">{step.title}</h5>
                                    <p className="text-sm text-slate-300 mb-3">{step.description}</p>
                                    
                                    <div className="flex flex-wrap gap-2">
                                      {step.estimated_time && (
                                        <span className="flex items-center gap-1 px-3 py-1 bg-slate-800 rounded-lg text-xs text-slate-300">
                                          <Clock className="w-3 h-3" />
                                          {step.estimated_time}
                                        </span>
                                      )}
                                      {step.difficulty && (
                                        <span className={`px-3 py-1 rounded-lg text-xs font-bold ${
                                          step.difficulty === 'hard' ? 'bg-red-500/20 text-red-300' :
                                          step.difficulty === 'medium' ? 'bg-yellow-500/20 text-yellow-300' :
                                          'bg-green-500/20 text-green-300'
                                        }`}>
                                          {step.difficulty}
                                        </span>
                                      )}
                                      {step.optional && (
                                        <span className="px-3 py-1 bg-blue-500/20 rounded-lg text-xs text-blue-300">
                                          Optional
                                        </span>
                                      )}
                                    </div>

                                    {step.success_criteria && (
                                      <div className="mt-3 p-3 bg-green-900/20 rounded-lg border border-green-500/30">
                                        <p className="text-xs text-green-300 flex items-center gap-2">
                                          <CheckCircle2 className="w-3 h-3" />
                                          {step.success_criteria}
                                        </p>
                                      </div>
                                    )}
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>

                          <div className="mt-4 flex items-center justify-between text-sm">
                            <span className="text-slate-400">Total Time: <span className="text-white font-bold">{plan.total_time}</span></span>
                            <span className="text-slate-400">Feasibility: <span className="text-white font-bold">{Math.round(plan.feasibility_score * 100)}%</span></span>
                          </div>
                        </div>
                      )
                    })}
                  </div>

                  {/* Risks */}
                  {results.plans.risks && results.plans.risks.length > 0 && (
                    <div className="mt-6 p-6 bg-yellow-900/20 rounded-2xl border border-yellow-500/30">
                      <h4 className="font-bold text-yellow-300 mb-4 flex items-center gap-2 text-lg">
                        <AlertTriangle className="w-5 h-5" />
                        Risk Analysis
                      </h4>
                      <div className="space-y-3">
                        {results.plans.risks.map((risk: any, index: number) => (
                          <div key={index} className="p-4 bg-slate-900/50 rounded-xl">
                            <div className="flex items-start justify-between mb-2">
                              <p className="text-white font-medium flex-1">{risk.risk}</p>
                              <div className="flex gap-2 ml-3">
                                <span className={`px-2 py-1 rounded text-xs font-bold ${
                                  risk.probability === 'high' ? 'bg-red-500/20 text-red-300' :
                                  risk.probability === 'medium' ? 'bg-yellow-500/20 text-yellow-300' :
                                  'bg-green-500/20 text-green-300'
                                }`}>
                                  {risk.probability}
                                </span>
                                <span className={`px-2 py-1 rounded text-xs font-bold ${
                                  risk.impact === 'high' ? 'bg-red-500/20 text-red-300' :
                                  risk.impact === 'medium' ? 'bg-yellow-500/20 text-yellow-300' :
                                  'bg-green-500/20 text-green-300'
                                }`}>
                                  {risk.impact} impact
                                </span>
                              </div>
                            </div>
                            <p className="text-sm text-green-400">Mitigation: {risk.mitigation}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Alternative Strategies */}
                  {results.plans.alternative_strategies && results.plans.alternative_strategies.length > 0 && (
                    <div className="mt-6">
                      <button
                        onClick={() => toggleSection('alternatives')}
                        className="w-full flex items-center justify-between p-4 bg-blue-900/20 rounded-xl border border-blue-500/30 hover:bg-blue-900/30 transition-all"
                      >
                        <span className="font-bold text-blue-300">Alternative Strategies ({results.plans.alternative_strategies.length})</span>
                        {expandedSections.alternatives ? <ChevronUp className="w-5 h-5 text-blue-400" /> : <ChevronDown className="w-5 h-5 text-blue-400" />}
                      </button>
                      {expandedSections.alternatives && (
                        <div className="mt-3 space-y-3">
                          {results.plans.alternative_strategies.map((alt: any, index: number) => (
                            <div key={index} className="p-4 bg-slate-900/50 rounded-xl border border-slate-700/50">
                              <p className="text-white font-bold mb-2">{alt.scenario}</p>
                              <p className="text-sm text-slate-300 mb-2">{alt.adjustments}</p>
                              <p className="text-xs text-slate-400">Trade-offs: {alt.trade_offs}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </motion.div>
              )}
              {/* FEATURE 5: Validation & Guardrails */}
              {results.validation && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                  className="bg-slate-800/50 backdrop-blur-xl rounded-3xl p-8 shadow-xl mb-6 border border-slate-700/50"
                >
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-4">
                      <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-red-500 to-rose-500 flex items-center justify-center shadow-lg">
                        <Shield className="w-7 h-7 text-white" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-white">Validation & Guardrails</h3>
                        <p className="text-sm text-slate-400">AI output safety and contradiction detection</p>
                      </div>
                    </div>
                    <div className="px-4 py-2 bg-red-500/20 rounded-xl border border-red-500/30">
                      <span className="text-sm font-bold text-red-300">Feature #5</span>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-3 gap-4 mb-6">
                    <div className={`p-5 rounded-2xl border-2 ${
                      results.validation.is_valid 
                        ? 'bg-green-900/20 border-green-500/50' 
                        : 'bg-red-900/20 border-red-500/50'
                    }`}>
                      <p className="text-xs font-bold uppercase tracking-wide mb-2 ${results.validation.is_valid ? 'text-green-300' : 'text-red-300'}">
                        Validation Status
                      </p>
                      <p className="text-2xl font-black text-white">
                        {results.validation.is_valid ? '✓ Valid' : '✗ Invalid'}
                      </p>
                    </div>

                    <div className="p-5 bg-blue-900/20 rounded-2xl border border-blue-500/30">
                      <p className="text-xs font-bold text-blue-300 uppercase tracking-wide mb-2">Validation Score</p>
                      <div className="flex items-center gap-3">
                        <div className="flex-1 h-3 bg-slate-700 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                            style={{ width: `${results.validation.validation_score * 100}%` }}
                          />
                        </div>
                        <span className="text-2xl font-black text-white">
                          {Math.round(results.validation.validation_score * 100)}%
                        </span>
                      </div>
                    </div>

                    <div className={`p-5 rounded-2xl border-2 ${
                      results.validation.safe_to_present 
                        ? 'bg-green-900/20 border-green-500/50' 
                        : 'bg-yellow-900/20 border-yellow-500/50'
                    }`}>
                      <p className="text-xs font-bold uppercase tracking-wide mb-2 ${results.validation.safe_to_present ? 'text-green-300' : 'text-yellow-300'}">
                        Safety Status
                      </p>
                      <p className="text-2xl font-black text-white">
                        {results.validation.safe_to_present ? '✓ Safe' : '⚠ Review'}
                      </p>
                    </div>
                  </div>

                  {results.validation.contradictions && results.validation.contradictions.length > 0 && (
                    <div className="mb-4 p-5 bg-red-900/20 rounded-2xl border border-red-500/30">
                      <h4 className="font-bold text-red-300 mb-4 flex items-center gap-2">
                        <AlertCircle className="w-5 h-5" />
                        Detected Contradictions ({results.validation.contradictions.length})
                      </h4>
                      <div className="space-y-3">
                        {results.validation.contradictions.map((contradiction: any, index: number) => (
                          <div key={index} className="p-4 bg-slate-900/50 rounded-xl border-l-4 border-red-500">
                            <div className="flex items-start justify-between mb-2">
                              <p className="text-white font-medium flex-1">{contradiction.description}</p>
                              <span className={`px-2 py-1 rounded text-xs font-bold ml-3 ${
                                contradiction.severity === 'critical' ? 'bg-red-500/30 text-red-300' :
                                contradiction.severity === 'high' ? 'bg-orange-500/30 text-orange-300' :
                                'bg-yellow-500/30 text-yellow-300'
                              }`}>
                                {contradiction.severity}
                              </span>
                            </div>
                            <p className="text-xs text-slate-400">Type: {contradiction.type}</p>
                            {contradiction.affected_steps && contradiction.affected_steps.length > 0 && (
                              <p className="text-xs text-slate-400 mt-1">
                                Affects steps: {contradiction.affected_steps.join(', ')}
                              </p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {results.validation.hallucinations && results.validation.hallucinations.length > 0 && (
                    <div className="mb-4 p-5 bg-orange-900/20 rounded-2xl border border-orange-500/30">
                      <h4 className="font-bold text-orange-300 mb-4 flex items-center gap-2">
                        <AlertTriangle className="w-5 h-5" />
                        Detected Hallucinations ({results.validation.hallucinations.length})
                      </h4>
                      <div className="space-y-3">
                        {results.validation.hallucinations.map((hallucination: any, index: number) => (
                          <div key={index} className="p-4 bg-slate-900/50 rounded-xl">
                            <p className="text-white font-medium mb-2">❌ {hallucination.claim}</p>
                            <p className="text-sm text-green-400">✓ Correction: {hallucination.correction}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {results.validation.feasibility_issues && results.validation.feasibility_issues.length > 0 && (
                    <div className="p-5 bg-yellow-900/20 rounded-2xl border border-yellow-500/30">
                      <h4 className="font-bold text-yellow-300 mb-4 flex items-center gap-2">
                        <AlertCircle className="w-5 h-5" />
                        Feasibility Issues ({results.validation.feasibility_issues.length})
                      </h4>
                      <div className="space-y-3">
                        {results.validation.feasibility_issues.map((issue: any, index: number) => (
                          <div key={index} className="p-4 bg-slate-900/50 rounded-xl">
                            <p className="text-white font-medium mb-2">{issue.issue}</p>
                            <p className="text-sm text-blue-400">→ Recommendation: {issue.recommendation}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {results.validation.requires_revision && (
                    <div className="mt-4 p-4 bg-red-900/20 rounded-xl border-l-4 border-red-500">
                      <p className="text-red-300 font-bold">⚠ This plan requires revision before implementation</p>
                    </div>
                  )}
                </motion.div>
              )}

              {/* Download Button */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
                className="flex justify-center gap-4"
              >
                <button
                  onClick={() => {
                    const dataStr = JSON.stringify(results, null, 2)
                    const dataBlob = new Blob([dataStr], { type: 'application/json' })
                    const url = URL.createObjectURL(dataBlob)
                    const link = document.createElement('a')
                    link.href = url
                    link.download = `intentos-analysis-${Date.now()}.json`
                    link.click()
                  }}
                  className="flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 text-white rounded-2xl font-bold hover:shadow-2xl hover:shadow-purple-500/50 hover:scale-105 transition-all"
                >
                  <Download className="w-5 h-5" />
                  Download Complete Analysis
                </button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Clarification Dialog */}
      {showClarification && clarificationData && clarificationData.clarification.clarification_questions && (
        <ClarificationDialog
          questions={clarificationData.clarification.clarification_questions}
          onSubmit={handleClarificationSubmit}
          onSkip={handleClarificationSkip}
        />
      )}

      {/* Footer */}
      <footer className="relative border-t border-slate-700/50 bg-slate-900/80 backdrop-blur-sm mt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-sm text-slate-400">
            <p className="font-medium">Built with ❤️ using Next.js, Tailwind CSS, and Google Gemini AI</p>
            <p className="mt-2">© 2024 IntentOS v2.1 - Advanced AI Decision Intelligence System</p>
            <p className="mt-2 text-xs text-slate-500">
              Interactive Clarification • Visual Analytics • 5 AI Features • Real-time Validation
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
