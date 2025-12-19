'use client'

import { motion } from 'framer-motion'
import { BarChart3, PieChart, TrendingUp } from 'lucide-react'

interface VisualizationChartsProps {
  intent: any
  constraints: any
  plans: any
}

export default function VisualizationCharts({ intent, constraints, plans }: VisualizationChartsProps) {
  // Calculate data for visualizations
  const confidenceData = [
    { label: 'Intent Clarity', value: intent.primary_intent?.confidence || 0 },
    { label: 'Constraint Understanding', value: constraints.skill_level ? 0.9 : 0.5 },
    { label: 'Plan Feasibility', value: plans.candidate_plans?.[0]?.feasibility_score || 0 },
  ]

  const planComparison = plans.candidate_plans?.map((plan: any) => ({
    name: plan.plan_id.replace('_', ' '),
    time: plan.constraint_satisfaction?.time || 0,
    skill: plan.constraint_satisfaction?.skill || 0,
    resources: plan.constraint_satisfaction?.resources || 0,
    feasibility: plan.feasibility_score || 0,
  })) || []

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-slate-800/50 backdrop-blur-xl rounded-3xl p-8 shadow-xl mb-6 border border-slate-700/50"
    >
      <div className="flex items-center gap-4 mb-8">
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center shadow-lg">
          <BarChart3 className="w-7 h-7 text-white" />
        </div>
        <div>
          <h3 className="text-2xl font-bold text-white">Analysis Visualizations</h3>
          <p className="text-sm text-slate-400">Data-driven insights for your plan</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Confidence Scores */}
        <div className="p-6 bg-slate-900/50 rounded-2xl border border-slate-700">
          <h4 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-cyan-400" />
            Confidence Metrics
          </h4>
          <div className="space-y-4">
            {confidenceData.map((item, index) => (
              <div key={index}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-slate-300 font-medium">{item.label}</span>
                  <span className="text-sm font-bold text-white">{Math.round(item.value * 100)}%</span>
                </div>
                <div className="h-3 bg-slate-700 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${item.value * 100}%` }}
                    transition={{ duration: 1, delay: index * 0.2 }}
                    className={`h-full ${
                      item.value > 0.8 ? 'bg-gradient-to-r from-green-500 to-emerald-500' :
                      item.value > 0.6 ? 'bg-gradient-to-r from-yellow-500 to-orange-500' :
                      'bg-gradient-to-r from-red-500 to-rose-500'
                    }`}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Plan Comparison */}
        <div className="p-6 bg-slate-900/50 rounded-2xl border border-slate-700">
          <h4 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <PieChart className="w-5 h-5 text-purple-400" />
            Plan Comparison
          </h4>
          <div className="space-y-4">
            {planComparison.map((plan: any, index: number) => (
              <div key={index} className="p-4 bg-slate-800/50 rounded-xl">
                <p className="text-sm font-bold text-white mb-3 capitalize">{plan.name}</p>
                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div>
                    <p className="text-slate-400 mb-1">Time</p>
                    <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-blue-500" 
                        style={{ width: `${plan.time * 100}%` }}
                      />
                    </div>
                  </div>
                  <div>
                    <p className="text-slate-400 mb-1">Skill</p>
                    <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-purple-500" 
                        style={{ width: `${plan.skill * 100}%` }}
                      />
                    </div>
                  </div>
                  <div>
                    <p className="text-slate-400 mb-1">Resources</p>
                    <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-green-500" 
                        style={{ width: `${plan.resources * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
                <div className="mt-3 flex items-center justify-between">
                  <span className="text-xs text-slate-400">Feasibility</span>
                  <span className="text-sm font-bold text-white">{Math.round(plan.feasibility * 100)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  )
}
