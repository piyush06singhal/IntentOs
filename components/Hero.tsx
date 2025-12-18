'use client'

import { motion } from 'framer-motion'
import { Target, Lightbulb, TrendingUp, Sparkles } from 'lucide-react'

export default function Hero() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="text-center mb-12"
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2, type: 'spring' }}
        className="inline-block mb-6"
      >
        <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center shadow-2xl shadow-purple-500/50 animate-float">
          <Target className="w-10 h-10 text-white" />
        </div>
      </motion.div>

      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="text-5xl md:text-7xl font-bold mb-6"
      >
        <span className="bg-gradient-to-r from-purple-600 via-pink-600 to-purple-600 bg-clip-text text-transparent animate-gradient">
          Transform Ideas
        </span>
        <br />
        <span className="text-gray-800">into Action Plans</span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto"
      >
        Don't know where to start? IntentOS uses AI to understand your goals,
        identify constraints, and create detailed action plans.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-12"
      >
        {[
          {
            icon: Lightbulb,
            title: 'Clarify Intent',
            description: 'Extract clear goals from vague descriptions',
            color: 'from-yellow-500 to-orange-500',
          },
          {
            icon: Target,
            title: 'Smart Planning',
            description: 'Generate step-by-step action plans',
            color: 'from-purple-500 to-pink-500',
          },
          {
            icon: TrendingUp,
            title: 'Track Progress',
            description: 'Monitor your journey to success',
            color: 'from-blue-500 to-cyan-500',
          },
        ].map((feature, index) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 + index * 0.1 }}
            className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:scale-105"
          >
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4`}>
              <feature.icon className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold mb-2 text-gray-800">{feature.title}</h3>
            <p className="text-sm text-gray-600">{feature.description}</p>
          </motion.div>
        ))}
      </motion.div>
    </motion.div>
  )
}
