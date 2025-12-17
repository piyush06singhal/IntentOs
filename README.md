# 🎯 IntentOS - AI Decision Intelligence System

Transform ambiguous ideas into clear, actionable plans with the power of AI.

![IntentOS](https://img.shields.io/badge/AI-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### Core Features
- **🎯 Intent Extraction**: Automatically understand what you want to achieve, even from vague descriptions
- **⚙️ Constraint Analysis**: Identify time, budget, skill, and resource constraints
- **❓ Smart Clarifications**: Ask intelligent questions to fill in the gaps
- **📋 Action Plans**: Generate detailed, step-by-step plans with timelines
- **🔄 Alternative Strategies**: Explore different approaches to achieve your goals
- **📊 Visual Analytics**: Interactive charts and progress tracking
- **💾 Session Management**: Save and load your analysis sessions
- **📤 Export Options**: Download plans as JSON or Markdown

### 🚀 Advanced Features (Elite AI Capabilities)
- **🎯 Multi-Intent Resolution**: Detects multiple goals and resolves conflicts intelligently
- **📊 Confidence Engine**: Asks questions only when needed, prevents over-questioning
- **⚖️ Plan Optimization**: Generates and scores multiple plans, selects the optimal one
- **🧠 Intent Memory**: Remembers your goals across sessions, detects intent drift
- **🛡️ Guardrail Validation**: Prevents hallucinations and contradictions, auto-corrects issues

[See detailed documentation →](ADVANCED_FEATURES.md)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd intentos
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your API key**

Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4-turbo-preview
TEMPERATURE=0.7
MAX_TOKENS=2000
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using Quick Start Scripts

**Windows:**
```bash
quickstart.bat
```

**Linux/Mac:**
```bash
chmod +x quickstart.sh
./quickstart.sh
```

## 📖 How It Works

IntentOS uses a multi-stage AI reasoning pipeline:

1. **Intent Extraction**: Analyzes your input to understand primary and secondary goals
2. **Constraint Parsing**: Identifies limitations and requirements
3. **Ambiguity Detection**: Finds unclear or missing information
4. **Clarification**: Asks targeted questions to resolve ambiguities
5. **Plan Generation**: Creates a detailed action plan with steps and timelines
6. **Alternative Strategies**: Suggests different approaches for various scenarios

## 💡 Example Use Cases

- **Learning**: "I want to learn machine learning but don't know where to start"
- **Projects**: "I need to build a mobile app for my startup"
- **Career**: "I want to transition from marketing to data science"
- **Business**: "I want to launch an online course but have limited budget"
- **Personal**: "I want to get fit but only have 30 minutes a day"

## 🎨 UI Features

### Modern Design
- Gradient backgrounds and smooth animations
- Responsive layout that works on all devices
- Dark mode support in sidebar

### Interactive Visualizations
- Confidence gauges for intent analysis
- Radar charts for constraint coverage
- Timeline visualizations for action plans
- Progress tracking with checkboxes

### Advanced Features
- Tab-based navigation for better organization
- Real-time session statistics
- Example prompts for quick start
- Comprehensive export options

## 📁 Project Structure

```
intentos/
├── app.py                      # Main Streamlit application
├── config/
│   ├── settings.py            # Configuration management
│   └── prompts.py             # LLM prompts
├── engine/
│   ├── intent_engine.py       # Intent extraction
│   ├── constraint_parser.py   # Constraint analysis
│   ├── ambiguity_detector.py  # Ambiguity detection
│   └── planner.py             # Action plan generation
├── ui/
│   ├── components.py          # Basic UI components
│   └── advanced_components.py # Advanced visualizations
├── utils/
│   ├── llm_client.py          # OpenAI API wrapper
│   └── session_manager.py     # Session save/load
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables (create this)
```

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add your OpenAI API key in Streamlit secrets
5. Deploy!

See [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) for detailed instructions.

## ⚙️ Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `MODEL_NAME`: GPT model to use (default: gpt-4-turbo-preview)
- `TEMPERATURE`: Response randomness 0-1 (default: 0.7)
- `MAX_TOKENS`: Maximum response length (default: 2000)

### App Settings (in sidebar)

- **Session Memory**: Maintain context across interactions
- **Confidence Threshold**: When to ask clarification questions (0-1)
- **Max Questions**: Maximum clarification questions (1-5)

## 🔒 Security

- Never commit your `.env` file to version control
- Use Streamlit secrets for cloud deployment
- Regularly rotate your API keys
- Monitor API usage in OpenAI dashboard
- Set spending limits to avoid unexpected charges

## 💰 Cost Considerations

- **Streamlit Cloud**: Free tier available
- **OpenAI API**: Pay per token
  - GPT-4 Turbo: ~$0.01 per 1K input tokens, ~$0.03 per 1K output tokens
  - Average analysis: $0.05-0.15 per session

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
black .
flake8 .
```

### Adding New Features

1. Create feature branch
2. Implement changes
3. Test thoroughly
4. Submit pull request

## 📚 Documentation

- [Architecture](ARCHITECTURE.md) - System design and components
- [Testing](TESTING.md) - Testing strategy and guidelines
- [Deployment](STREAMLIT_DEPLOYMENT.md) - Deployment instructions
- [Examples](EXAMPLES.md) - Usage examples and patterns

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [OpenAI GPT-4](https://openai.com)
- Visualizations by [Plotly](https://plotly.com)

## 📧 Support

- Issues: [GitHub Issues](your-repo-url/issues)
- Discussions: [GitHub Discussions](your-repo-url/discussions)

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Integration with project management tools
- [ ] Team collaboration features
- [ ] Custom AI model fine-tuning
- [ ] Mobile app version
- [ ] Voice input support

---

Made with ❤️ by the IntentOS team

**IntentOS**

An AI decision intelligence system that transforms vague user intent into structured, actionable plans.

## Architecture

IntentOS uses a multi-stage reasoning pipeline:

1. **Input Normalization** - Clean and structure raw user input
2. **Intent & Entity Extraction** - Identify primary/secondary intents with confidence scores
3. **Constraint Analysis** - Extract time, skill, resources, urgency, preferences
4. **Ambiguity Detection** - Identify missing information and conflicts
5. **Clarification Strategy** - Generate high-value follow-up questions
6. **Action Planning** - Create optimized step-by-step plans with alternatives

## Project Structure

```
intentos/
├── app.py                      # Main Streamlit application
├── config/
│   ├── prompts.py             # All LLM prompt templates
│   └── settings.py            # Configuration and environment variables
├── engine/
│   ├── intent_engine.py       # Intent detection and extraction
│   ├── constraint_parser.py   # Constraint analysis
│   ├── ambiguity_detector.py  # Ambiguity and gap detection
│   └── planner.py             # Action plan generation
├── ui/
│   └── components.py          # Reusable UI components
├── utils/
│   └── llm_client.py          # LLM abstraction layer
├── requirements.txt
└── .env.example
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the application:
```bash
streamlit run app.py
```

## Environment Variables

- `OPENAI_API_KEY` - OpenAI API key (required)
- `MODEL_NAME` - Model to use (default: gpt-4-turbo-preview)
- `TEMPERATURE` - Model temperature (default: 0.7)
- `MAX_TOKENS` - Max tokens per response (default: 2000)

## Features

- **Intent Detection** - Identifies primary and secondary intents with confidence scores
- **Constraint Extraction** - Automatically extracts time, skill level, resources, urgency
- **Smart Clarification** - Asks only high-value questions (max 3)
- **Action Planning** - Generates step-by-step plans optimized for constraints
- **Alternative Strategies** - Provides options for different scenarios
- **Session Memory** - Maintains context across interactions

## Design Philosophy

IntentOS is designed to feel like a professional AI consultant, not a chatbot. It:
- Never assumes missing data
- Asks clarifying questions before hallucinating
- Prioritizes usefulness over verbosity
- Produces structured, actionable outputs
