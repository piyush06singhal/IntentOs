import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'IntentOS v2.0 - AI Decision Intelligence System',
  description: 'Advanced AI system with 5 features: Multi-Intent Analysis, Clarification Engine, Multi-Plan Optimization, Memory, and Validation Guardrails',
  keywords: 'AI, decision intelligence, intent analysis, action planning, machine learning',
  authors: [{ name: 'IntentOS Team' }],
  openGraph: {
    title: 'IntentOS v2.0 - AI Decision Intelligence',
    description: 'Transform ambiguity into action with advanced AI',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
