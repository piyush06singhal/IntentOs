# IntentOS v2.0 - Advanced AI Decision Intelligence System

![IntentOS Banner](https://img.shields.io/badge/IntentOS-v2.0-purple?style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=for-the-badge&logo=typescript)
![Gemini AI](https://img.shields.io/badge/Gemini-AI-orange?style=for-the-badge)

## 🎯 What is IntentOS?

IntentOS is a production-grade AI system that transforms ambiguous human intent into structured, actionable plans. Unlike simple chatbots, IntentOS uses a **5-stage reasoning pipeline** to understand what users actually want, detect conflicts, ask intelligent questions, and generate optimized action plans.

## 🚀 5 Advanced Features

### 1. 🌳 Multi-Intent Decomposition with Conflict Resolution

**What it does:**
- Detects primary, secondary, and hidden goals in user input
- Identifies conflicts between goals (time, resources, priorities)
- Provides resolution strategies for each conflict

**Why it matters:**
Real users never have single, clean intents. This feature handles real-world ambiguity.

**Example:**
```
Input: "I want to learn ML and build a startup while working full-time"
Output:
- Primary: Learn machine learning
- Secondary: Build startup, Maintain job
- Conflict: Time constraint (critical severity)
- Resolution: Phased approach with weekend focus
```

### 2. 💡 Confidence-Driven Clarification Engine

**What it does:**
- Assigns confidence scores to inferred intents
- Only asks follow-up questions when confidence < 75%
- Limits to maximum 3 high-impact questions
- Can proceed with stated assumptions if user doesn't answer

**Why it matters:**
Most AI systems annoy users by over-asking. This shows decision intelligence.

**Example:**
```
Confidence: 65% → Asks 2 clarification questions
Confidence: 85% → Proceeds without questions
```

### 3. 🎯 Constraint-Aware Plan Optimization

**What it does:**
- Generates 3 candidate plans: Optimal, Fast Track, Thorough
- Scores each plan against constraints (time, skill, resources)
- Automatically selects the best plan
- Provides alternative strategies for different scenarios

**Why it matters:**
Moves from advice → optimization. Mirrors real planning engines.

**Plans Generated:**
- **Optimal Plan**: Best balance of all constraints
- **Fast Track**: Prioritizes speed over depth
- **Thorough Plan**: Prioritizes quality/learning over speed

### 4. 🧠 Persistent Intent Memory with Drift Detection

**What it does:**
- Remembers user goals across sessions (last 5 stored)
- Detects when intent changes over time
- Adapts plans based on intent evolution
- Tracks drift types: expansion, pivot, refinement

**Why it matters:**
Demonstrates long-term reasoning, a key LLM challenge.

**Storage:**
- Uses localStorage for client-side persistence
- Passed to AI for context-aware analysis

### 5. 🛡️ Hallucination & Contradiction Guardrail Layer

**What it does:**
- Validates outputs against extracted constraints
- Detects contradictions before showing results
- Identifies hallucinations (unfounded assumptions)
- Flags feasibility issues with recommendations
- Provides safety score and validation status

**Why it matters:**
Proves understanding of LLM failure modes and safe system design.

**Validation Checks:**
- Time estimates vs available time
- Required skills vs user level
- Resources mentioned vs user resources
- Logic contradictions
- Unrealistic assumptions

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT                                │
│         "I want to learn ML but don't know where to start"  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1: Multi-Intent Decomposition                        │
│  → Primary, Secondary, Hidden Intents                       │
│  → Conflict Detection & Resolution                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 2: Constraint Extraction                             │
│  → Time, Skill, Resources, Preferences                      │
│  → Blockers & Context                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 3: Clarification Strategy                            │
│  → Confidence Scoring                                       │
│  → Intelligent Question Generation                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 4: Multi-Plan Generation                             │
│  → 3 Candidate Plans (Optimal, Fast, Thorough)             │
│  → Constraint Satisfaction Scoring                          │
│  → Risk Analysis & Alternatives                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 5: Validation & Guardrails                           │
│  → Contradiction Detection                                  │
│  → Hallucination Prevention                                 │
│  → Feasibility Validation                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              STRUCTURED OUTPUT                               │
│  → Validated Action Plans                                   │
│  → Risk Analysis                                            │
│  → Alternative Strategies                                   │
└─────────────────────────────────────────────────────────────┘
```

## 🎨 UI/UX Design

### Design Philosophy
- **Minimal & Professional**: Clean, modern interface
- **Dark Theme**: Slate/Indigo color palette for reduced eye strain
- **AI Dashboard Aesthetic**: Feels like enterprise software
- **Clear Separation**: Reasoning vs output clearly distinguished

### Key UI Components
1. **Hero Section**: Animated logo, feature badges, examples
2. **Input Area**: Large textarea with smart examples
3. **Pipeline Status**: Real-time processing indicators
4. **Feature Cards**: Each of 5 features has dedicated section
5. **Collapsible Sections**: Expandable for detailed information
6. **Download**: Export complete analysis as JSON

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **AI Model**: Google Gemini 2.5 Flash
- **Icons**: Lucide React
- **Deployment**: Vercel

## 📦 Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd intentos

# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Add your GEMINI_API_KEY to .env.local

# Run development server
npm run dev
```

Visit `http://localhost:3000`

## 🔑 Environment Variables

Create `.env.local`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

## 🚀 Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Add `GEMINI_API_KEY` environment variable
4. Deploy

### Manual Deployment

```bash
npm run build
npm start
```

## 📊 Example Use Cases

### 1. Career Transition
```
Input: "I want to transition from marketing to data science within a year"
Output:
- Multi-intent: Career change + skill acquisition + job search
- Conflicts: Time constraint vs learning depth
- 3 Plans: 6-month intensive, 12-month balanced, 18-month thorough
- Validation: Checks realistic timeline for skill level
```

### 2. Startup Launch
```
Input: "I need to build a mobile app with no coding experience and $5k budget"
Output:
- Multi-intent: Learn to code + build app + launch product
- Conflicts: Skill level vs timeline, budget vs quality
- 3 Plans: No-code solution, learn React Native, hire developer
- Validation: Flags unrealistic expectations
```

### 3. Learning Path
```
Input: "I want to learn machine learning but only have 5 hours per week"
Output:
- Multi-intent: Learn ML + manage time + apply knowledge
- Constraints: 5 hrs/week, beginner level
- 3 Plans: 6-month fundamentals, 12-month comprehensive, 3-month basics
- Validation: Ensures time estimates match availability
```

## 🧪 Testing the Features

### Test Multi-Intent Detection
```
Try: "I want to learn Python, build a portfolio, and get a job in 3 months"
Expected: Detects 3 intents + time conflict
```

### Test Clarification Engine
```
Try: "I want to learn something technical"
Expected: Low confidence → asks clarification questions
```

### Test Multi-Plan Generation
```
Try: "I want to learn web development with 10 hours per week"
Expected: 3 different plans with time estimates
```

### Test Memory & Drift
```
1. Analyze: "I want to learn React"
2. Analyze: "Actually, I want to learn Vue instead"
Expected: Detects intent drift (pivot)
```

### Test Validation
```
Try: "I want to become an expert ML engineer in 2 weeks"
Expected: Validation flags unrealistic timeline
```

## 📁 Project Structure

```
intentos/
├── app/
│   ├── api/
│   │   └── analyze/
│   │       └── route.ts          # 5-stage pipeline API
│   ├── globals.css               # Dark theme styling
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Main UI with all features
├── lib/
│   ├── api.ts                    # API client
│   ├── gemini.ts                 # Gemini AI integration
│   └── prompts.ts                # Advanced prompt templates
├── components/                   # (Optional) Reusable components
├── .env.local.example           # Environment template
├── package.json                 # Dependencies
├── tailwind.config.ts           # Tailwind configuration
├── tsconfig.json                # TypeScript configuration
└── README.md                    # This file
```

## 🎯 Key Differentiators

1. **Not a Chatbot**: Multi-stage reasoning pipeline, not single LLM call
2. **Production-Ready**: Error handling, validation, type safety
3. **Real-World Focus**: Handles ambiguity, conflicts, missing data
4. **Consultative**: Asks smart questions, provides alternatives
5. **Safe**: Validates outputs, prevents hallucinations

## 🔮 Future Enhancements

- [ ] User authentication & persistent storage
- [ ] Plan execution tracking
- [ ] Collaborative planning (team mode)
- [ ] Integration with project management tools
- [ ] Mobile app version
- [ ] Voice input support
- [ ] Multi-language support

## 📝 License

MIT License - feel free to use for personal or commercial projects

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Contact

Built with ❤️ for AI engineers and product builders

---

**IntentOS v2.0** - Transform ambiguity into action.
