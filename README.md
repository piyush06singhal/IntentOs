# 🎯 IntentOS - AI Decision Intelligence System

Transform ambiguous ideas into clear, actionable plans with AI.

![Next.js](https://img.shields.io/badge/Next.js-14-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)
![Tailwind](https://img.shields.io/badge/Tailwind-3-cyan)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black)

## ✨ Features

- 🎨 **Beautiful Modern UI** - Gradient designs, smooth animations, responsive
- ⚡ **Lightning Fast** - Built with Next.js 14 App Router
- 🤖 **AI-Powered** - Google Gemini Pro for intelligent analysis
- 📱 **Mobile-First** - Works perfectly on all devices
- 🚀 **Production-Ready** - Optimized for Vercel deployment

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Add your Gemini API key
cp .env.local.example .env.local
# Edit .env.local and add: GEMINI_API_KEY=your_key_here

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## 📦 Deploy to Vercel

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

### Manual Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Add environment variable in Vercel dashboard:
# GEMINI_API_KEY=your_key_here
```

## 🔑 Get Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to `.env.local` or Vercel environment variables

## 🎨 Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **AI**: Google Gemini Pro
- **Deployment**: Vercel

## 📁 Project Structure

```
├── app/
│   ├── api/analyze/route.ts    # API endpoint
│   ├── globals.css             # Global styles
│   ├── layout.tsx              # Root layout
│   └── page.tsx                # Home page
├── components/
│   ├── Hero.tsx                # Hero section
│   ├── InputSection.tsx        # Input form
│   └── AnalysisResults.tsx     # Results display
├── lib/
│   ├── api.ts                  # API client
│   ├── gemini.ts               # Gemini integration
│   └── prompts.ts              # AI prompts
└── package.json
```

## 🎯 How It Works

1. **User Input** - Describe your goal (can be vague!)
2. **AI Analysis** - Gemini extracts intent and constraints
3. **Plan Generation** - Creates detailed step-by-step action plan
4. **Download** - Export your plan as JSON

## 🔧 Development

```bash
npm run dev      # Start dev server
npm run build    # Build for production
npm start        # Start production server
npm run lint     # Lint code
```

## 🐛 Troubleshooting

**API Key Issues?**
- Make sure `GEMINI_API_KEY` is set in `.env.local` (local) or Vercel (production)
- Get a free key at https://makersuite.google.com/app/apikey

**Rate Limits?**
- Gemini Pro free tier: 60 requests/minute
- Wait a minute or upgrade your API key

## 📝 License

MIT License

## 🙏 Credits

Built with Next.js, Tailwind CSS, Framer Motion, and Google Gemini AI

---

**Made with ❤️ for better decision making**
