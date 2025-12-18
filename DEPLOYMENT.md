# IntentOS v2.0 - Deployment Guide

## 🚀 Quick Deploy to Vercel (Recommended)

### Prerequisites
- GitHub account
- Vercel account (free tier works)
- Google Gemini API key

### Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "IntentOS v2.0 - Advanced AI Decision Intelligence"
git push origin main
```

2. **Deploy to Vercel**
- Go to [vercel.com](https://vercel.com)
- Click "New Project"
- Import your GitHub repository
- Configure:
  - Framework Preset: Next.js
  - Root Directory: ./
  - Build Command: `npm run build`
  - Output Directory: .next

3. **Add Environment Variables**
In Vercel project settings → Environment Variables:
```
GEMINI_API_KEY=your_actual_api_key_here
```

4. **Deploy**
- Click "Deploy"
- Wait 2-3 minutes
- Your app is live! 🎉

## 🔧 Manual Deployment

### Option 1: Node.js Server

```bash
# Build the application
npm run build

# Start production server
npm start
```

Server runs on `http://localhost:3000`

### Option 2: Docker

Create `Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

Build and run:
```bash
docker build -t intentos .
docker run -p 3000:3000 -e GEMINI_API_KEY=your_key intentos
```

### Option 3: PM2 (Production Process Manager)

```bash
# Install PM2
npm install -g pm2

# Build
npm run build

# Start with PM2
pm2 start npm --name "intentos" -- start

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup
```

## 🌐 Deployment Platforms

### Vercel (Recommended)
- ✅ Zero configuration
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Serverless functions
- ✅ Free tier available

### Netlify
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build
npm run build

# Deploy
netlify deploy --prod
```

### AWS Amplify
1. Connect GitHub repository
2. Configure build settings:
   - Build command: `npm run build`
   - Output directory: `.next`
3. Add environment variables
4. Deploy

### Railway
1. Connect GitHub repository
2. Add `GEMINI_API_KEY` environment variable
3. Railway auto-detects Next.js
4. Deploy

### DigitalOcean App Platform
1. Create new app from GitHub
2. Configure:
   - Type: Web Service
   - Build Command: `npm run build`
   - Run Command: `npm start`
3. Add environment variables
4. Deploy

## 🔐 Security Checklist

- [ ] API key stored in environment variables (never in code)
- [ ] `.env.local` added to `.gitignore`
- [ ] HTTPS enabled (automatic on Vercel)
- [ ] Rate limiting configured (optional)
- [ ] CORS configured if needed
- [ ] Error messages don't expose sensitive data

## ⚡ Performance Optimization

### 1. Enable Caching
Add to `next.config.js`:
```javascript
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=3600, must-revalidate',
          },
        ],
      },
    ]
  },
}
```

### 2. Image Optimization
Already configured with Next.js Image component

### 3. API Response Caching
Consider implementing Redis for frequently requested analyses

### 4. CDN Configuration
Vercel automatically uses CDN. For other platforms:
- Use Cloudflare
- Configure CloudFront (AWS)
- Use Fastly

## 📊 Monitoring & Analytics

### Vercel Analytics
```bash
npm install @vercel/analytics
```

Add to `app/layout.tsx`:
```typescript
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

### Error Tracking (Sentry)
```bash
npm install @sentry/nextjs
```

Configure `sentry.client.config.js` and `sentry.server.config.js`

### Custom Logging
Add to API routes:
```typescript
console.log({
  timestamp: new Date().toISOString(),
  stage: 'multi-intent',
  confidence: intentAnalysis.primary_intent.confidence,
  userId: 'anonymous',
})
```

## 🧪 Testing Before Deployment

### 1. Build Test
```bash
npm run build
```
Should complete without errors

### 2. Production Test
```bash
npm run build
npm start
```
Test all features locally

### 3. Environment Variables Test
```bash
# Test with production env vars
GEMINI_API_KEY=test_key npm run dev
```

### 4. Lighthouse Audit
- Open Chrome DevTools
- Run Lighthouse audit
- Target scores:
  - Performance: >90
  - Accessibility: >95
  - Best Practices: >95
  - SEO: >90

## 🔄 CI/CD Pipeline

### GitHub Actions
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 🐛 Troubleshooting

### Build Fails
```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run build
```

### API Key Not Working
- Check environment variable name: `GEMINI_API_KEY`
- Verify key is valid at https://makersuite.google.com
- Restart development server after adding env vars

### Deployment Timeout
- Increase timeout in `vercel.json`:
```json
{
  "functions": {
    "app/api/**/*.ts": {
      "maxDuration": 60
    }
  }
}
```

### Memory Issues
- Increase Node.js memory:
```json
{
  "scripts": {
    "build": "NODE_OPTIONS='--max-old-space-size=4096' next build"
  }
}
```

## 📈 Scaling Considerations

### For High Traffic
1. **API Rate Limiting**
   - Implement rate limiting per IP
   - Use Redis for distributed rate limiting

2. **Caching Layer**
   - Cache similar queries
   - Use Redis or Memcached

3. **Load Balancing**
   - Deploy multiple instances
   - Use Vercel's automatic scaling

4. **Database**
   - Add PostgreSQL for user data
   - Store session history in DB instead of localStorage

5. **Queue System**
   - Use Bull or BullMQ for long-running analyses
   - Implement webhook callbacks

## 🎯 Post-Deployment Checklist

- [ ] Application loads correctly
- [ ] All 5 features working
- [ ] API calls successful
- [ ] No console errors
- [ ] Mobile responsive
- [ ] HTTPS enabled
- [ ] Environment variables set
- [ ] Error tracking configured
- [ ] Analytics enabled
- [ ] Performance metrics acceptable
- [ ] SEO meta tags present
- [ ] Social sharing works

## 📞 Support

If you encounter issues:
1. Check Vercel deployment logs
2. Review browser console for errors
3. Verify API key is valid
4. Check Gemini API quota/limits
5. Review this deployment guide

## 🎉 Success!

Your IntentOS v2.0 is now live and ready to transform ambiguity into action!

Share your deployment URL and start helping users make better decisions.

---

**Need help?** Open an issue on GitHub or check the main README.md
