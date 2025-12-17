"""Landing page and welcome components."""
import streamlit as st

def render_welcome_hero():
    """Render an attractive hero section for first-time users."""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 3rem 2rem; border-radius: 20px; color: white; margin-bottom: 2rem;
                box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);'>
        <div style='text-align: center;'>
            <h1 style='color: white; font-size: 3.5rem; margin: 0; font-weight: 700;'>
                🎯 Welcome to IntentOS
            </h1>
            <p style='font-size: 1.3rem; margin: 1rem 0 0 0; opacity: 0.95; font-weight: 400;'>
                Transform Your Ambiguous Ideas into Clear, Actionable Plans
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_feature_cards():
    """Render feature highlight cards."""
    st.markdown("### ✨ What IntentOS Can Do For You")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); height: 100%;
                    border-left: 4px solid #667eea;'>
            <h3 style='color: #667eea; margin-top: 0;'>🎯 Clarify Intent</h3>
            <p style='color: #64748b;'>
                Don't know exactly what you want? No problem. 
                IntentOS extracts clear goals from vague descriptions.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); height: 100%;
                    border-left: 4px solid #764ba2;'>
            <h3 style='color: #764ba2; margin-top: 0;'>📋 Create Plans</h3>
            <p style='color: #64748b;'>
                Get detailed, step-by-step action plans with timelines, 
                resources, and success criteria.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); height: 100%;
                    border-left: 4px solid #667eea;'>
            <h3 style='color: #667eea; margin-top: 0;'>🔄 Explore Options</h3>
            <p style='color: #64748b;'>
                Discover alternative strategies and approaches 
                tailored to your constraints.
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_example_prompts():
    """Render example prompt buttons."""
    st.markdown("### 💡 Try These Examples")
    st.caption("Click any example to get started instantly")
    
    examples = [
        {
            "emoji": "🎓",
            "title": "Learn a New Skill",
            "prompt": "I want to learn machine learning but I'm not sure where to start. I have some Python experience and can dedicate 10 hours per week.",
            "color": "#3b82f6"
        },
        {
            "emoji": "🚀",
            "title": "Start a Project",
            "prompt": "I want to build a mobile app for tracking fitness goals but I don't know what tech stack to use. I have a $5000 budget and 3 months.",
            "color": "#8b5cf6"
        },
        {
            "emoji": "💼",
            "title": "Career Change",
            "prompt": "I want to transition from marketing to data science within the next year. I have a business degree but no technical background.",
            "color": "#ec4899"
        },
        {
            "emoji": "💰",
            "title": "Start a Business",
            "prompt": "I want to launch an online course teaching photography but I'm not sure how to market it or what platform to use.",
            "color": "#f59e0b"
        },
        {
            "emoji": "🏋️",
            "title": "Get Fit",
            "prompt": "I want to lose 20 pounds and build muscle but I only have 30 minutes a day and can't afford a gym membership.",
            "color": "#10b981"
        },
        {
            "emoji": "📚",
            "title": "Write a Book",
            "prompt": "I want to write and publish a science fiction novel but I've never written fiction before and work full-time.",
            "color": "#6366f1"
        }
    ]
    
    cols = st.columns(3)
    
    for i, example in enumerate(examples):
        with cols[i % 3]:
            button_html = f"""
            <div style='margin-bottom: 1rem;'>
                <button style='
                    width: 100%;
                    padding: 1rem;
                    background: linear-gradient(135deg, {example["color"]} 0%, {example["color"]}dd 100%);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    font-size: 1rem;
                    font-weight: 600;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                    transition: transform 0.2s;
                    text-align: left;
                ' onmouseover='this.style.transform="translateY(-2px)"' 
                   onmouseout='this.style.transform="translateY(0)"'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{example["emoji"]}</div>
                    <div>{example["title"]}</div>
                </button>
            </div>
            """
            
            if st.button(f"{example['emoji']} {example['title']}", key=f"example_{i}", use_container_width=True):
                st.session_state.example_input = example["prompt"]
                st.rerun()

def render_how_it_works():
    """Render the 'How It Works' section."""
    st.markdown("### 🔄 How It Works")
    
    steps = [
        {
            "number": "1",
            "title": "Describe Your Goal",
            "description": "Tell us what you want to achieve. Be as vague or specific as you like.",
            "icon": "💭"
        },
        {
            "number": "2",
            "title": "AI Analysis",
            "description": "Our AI extracts your intent, identifies constraints, and detects ambiguities.",
            "icon": "🤖"
        },
        {
            "number": "3",
            "title": "Clarification",
            "description": "Answer a few smart questions to help us understand your needs better.",
            "icon": "❓"
        },
        {
            "number": "4",
            "title": "Get Your Plan",
            "description": "Receive a detailed action plan with steps, timelines, and alternatives.",
            "icon": "📋"
        }
    ]
    
    cols = st.columns(4)
    
    for i, step in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem;'>
                <div style='
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 1rem auto;
                    font-size: 2rem;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                '>
                    {step["icon"]}
                </div>
                <h4 style='color: #1e293b; margin: 0.5rem 0;'>{step["title"]}</h4>
                <p style='color: #64748b; font-size: 0.9rem; margin: 0;'>
                    {step["description"]}
                </p>
            </div>
            """, unsafe_allow_html=True)

def render_stats_banner():
    """Render a stats banner."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: white; 
                    border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-size: 2rem; color: #667eea; font-weight: 700;'>AI</div>
            <div style='color: #64748b; font-size: 0.9rem;'>Powered</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: white; 
                    border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-size: 2rem; color: #764ba2; font-weight: 700;'>5</div>
            <div style='color: #64748b; font-size: 0.9rem;'>Analysis Stages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: white; 
                    border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-size: 2rem; color: #667eea; font-weight: 700;'>∞</div>
            <div style='color: #64748b; font-size: 0.9rem;'>Use Cases</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: white; 
                    border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <div style='font-size: 2rem; color: #764ba2; font-weight: 700;'>Free</div>
            <div style='color: #64748b; font-size: 0.9rem;'>To Use</div>
        </div>
        """, unsafe_allow_html=True)
