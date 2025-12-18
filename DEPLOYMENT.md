# 🚀 Deployment Guide

## ✅ Security Checklist

- ✅ API keys are in `.gitignore`
- ✅ `.env.local` is NOT committed to GitHub
- ✅ Only `.env.local.example` is in the repo (without real keys)
- ✅ All sensitive data excluded from version control

## 📦 Deploy to Vercel (Recommended)

### Step 1: Install Dependencies

```bash
npm install
```

### Step 2: Test Locally

```bash
# Create .env.local file
cp .env.local.example .env.local

# Add your Gemini API key
# Edit .env.local: GEMINI_API_KEY=your_key_here

# Run dev server
npm run dev
```

### Step 3: Deploy to Vercel

**Option A: Vercel Dashboard**

1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository: `piyush06singhal/IntentOs`
4. Vercel will auto-detect Next.js
5. Add Environment Variable:
   - Key: `GEMINI_API_KEY`
   - Value: Your Gemini API key (get from https://makersuite.google.com/app/apikey)
6. Click "Deploy"

**Option B: Vercel CLI**

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Add environment variable
vercel env add GEMINI_API_KEY production
# Paste your Gemini API key when prompted
```

### Step 4: Verify Deployment

1. Visit your Vercel URL (e.g., `intentos.vercel.app`)
2. Test the app with a sample goal
3. Check if analysis works

## 🔑 Get New Gemini API Key (If Needed)

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to Vercel environment variables

## 🐛 Troubleshooting

### Build Fails

```bash
# Clear cache locally
rm -rf .next node_modules
npm install
npm run build
```

### API Key Not Working

- Make sure `GEMINI_API_KEY` is added in Vercel Dashboard → Settings → Environment Variables
- Redeploy after adding the key
- Check if the key is valid at https://makersuite.google.com

### Rate Limit Errors

- Gemini Pro free tier: 60 requests/minute
- Wait a minute between requests
- Or upgrade your API key

## 📊 What Was Built

### Removed (Old Streamlit Version)
- ❌ Python backend (app.py, config/, engine/, ui/, utils/)
- ❌ Streamlit dependencies
- ❌ All .py files
- ❌ requirements.txt

### Added (New Next.js Version)
- ✅ Next.js 14 with App Router
- ✅ TypeScript for type safety
- ✅ Tailwind CSS for styling
- ✅ Framer Motion for animations
- ✅ Modern, responsive UI
- ✅ API routes for backend
- ✅ Vercel-optimized configuration

### File Structure
```
IntentOs/
├── app/
│   ├── api/analyze/route.ts    # Backend API
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx                # Main page
├── components/
│   ├── Hero.tsx
│   ├── InputSection.tsx
│   └── AnalysisResults.tsx
├── lib/
│   ├── api.ts
│   ├── gemini.ts
│   └── prompts.ts
├── .env.local.example          # Template (no real keys)
├── .gitignore                  # Excludes .env.local
├── package.json
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── vercel.json
```

## 🎯 Features

- 🎨 Beautiful gradient UI with purple/pink theme
- ⚡ Fast Next.js 14 performance
- 📱 Fully responsive (mobile, tablet, desktop)
- 🤖 AI-powered analysis with Gemini Pro
- 💾 Download plans as JSON
- 🔄 Smooth animations with Framer Motion
- ✨ Modern glass morphism effects

## 📈 Next Steps

After deployment:

1. ✅ Test the live app
2. ✅ Share the URL
3. ✅ Monitor usage in Vercel dashboard
4. ✅ Check Gemini API usage at https://ai.dev/usage

## 🔒 Security Notes

- ✅ API key is stored in Vercel environment variables (encrypted)
- ✅ Not exposed in client-side code
- ✅ Not committed to GitHub
- ✅ Only used in server-side API routes

---

**Your IntentOS is now production-ready! 🎉**
