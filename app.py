"""IntentOS - AI Decision Intelligence System

Main Streamlit application that orchestrates the multi-stage reasoning pipeline.
"""
import streamlit as st
from typing import Dict, Any

# Import engine components
from engine.intent_engine import intent_engine
from engine.constraint_parser import constraint_parser
from engine.ambiguity_detector import ambiguity_detector
from engine.planner import planner

# Import UI components
from ui.components import (
    render_sidebar,
    render_intent_breakdown,
    render_constraint_analysis,
    render_clarification_questions,
    render_action_plan,
    render_alternative_strategies,
    show_loading_message,
    show_error,
    show_success
)

# Import advanced UI components
from ui.advanced_components import (
    render_progress_tracker,
    render_timeline_visualization,
    render_confidence_gauge,
    render_constraint_radar,
    render_export_options,
    render_stats_dashboard
)

# Import landing page components
from ui.landing import (
    render_welcome_hero,
    render_feature_cards,
    render_example_prompts,
    render_how_it_works,
    render_stats_banner
)

# Import configuration
from config.settings import settings
from utils.session_manager import session_manager

# Page configuration
st.set_page_config(
    page_title="IntentOS",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin: 2rem auto;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stTextArea>div>div>textarea {
        background-color: white;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    h1 {
        color: #1e293b;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2, h3 {
        color: #334155;
        font-weight: 600;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .stExpander {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    div[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    div[data-testid="stSidebar"] .stButton>button {
        background-color: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    div[data-testid="stSidebar"] .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.3);
    }
    
    .success-box {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "input_history" not in st.session_state:
        st.session_state.input_history = []
    if "current_stage" not in st.session_state:
        st.session_state.current_stage = "input"
    if "intent_data" not in st.session_state:
        st.session_state.intent_data = None
    if "constraint_data" not in st.session_state:
        st.session_state.constraint_data = None
    if "ambiguity_data" not in st.session_state:
        st.session_state.ambiguity_data = None
    if "clarification_questions" not in st.session_state:
        st.session_state.clarification_questions = []
    if "clarification_responses" not in st.session_state:
        st.session_state.clarification_responses = {}
    if "plan_data" not in st.session_state:
        st.session_state.plan_data = None
    if "alternatives" not in st.session_state:
        st.session_state.alternatives = []
    if "use_memory" not in st.session_state:
        st.session_state.use_memory = True
    if "confidence_threshold" not in st.session_state:
        st.session_state.confidence_threshold = 0.6
    if "completed_steps" not in st.session_state:
        st.session_state.completed_steps = set()
    if "current_user_input" not in st.session_state:
        st.session_state.current_user_input = ""

def load_saved_session(filename: str):
    """Load a saved session into the current state."""
    try:
        session_data = session_manager.load_session(filename)
        
        st.session_state.intent_data = session_data.get("intent")
        st.session_state.constraint_data = session_data.get("constraints")
        st.session_state.plan_data = session_data.get("plan")
        st.session_state.alternatives = session_data.get("alternatives", [])
        st.session_state.current_user_input = session_data.get("user_input", "")
        st.session_state.current_stage = "complete"
        
        st.success(f"✅ Loaded session from {session_data.get('timestamp', 'unknown time')}")
    except Exception as e:
        st.error(f"Failed to load session: {str(e)}")

def process_user_input(user_input: str):
    """
    Process user input through the multi-stage reasoning pipeline.
    
    Pipeline stages:
    1. Intent Extraction
    2. Constraint Parsing
    3. Ambiguity Detection
    4. Clarification (if needed)
    5. Action Plan Generation
    6. Alternative Strategies
    """
    try:
        # Stage 1: Intent Extraction
        with show_loading_message("🔍 Analyzing your intent..."):
            intent_data = intent_engine.extract_intent(user_input)
            st.session_state.intent_data = intent_data
        
        # Stage 2: Constraint Parsing
        with show_loading_message("⚙️ Extracting constraints..."):
            constraint_data = constraint_parser.extract_constraints(user_input)
            st.session_state.constraint_data = constraint_data
        
        # Stage 3: Ambiguity Detection
        with show_loading_message("🔎 Checking for ambiguities..."):
            ambiguity_data = ambiguity_detector.detect_ambiguity(
                user_input,
                intent_data,
                constraint_data
            )
            st.session_state.ambiguity_data = ambiguity_data
        
        # Stage 4: Clarification (if needed)
        if ambiguity_detector.should_ask_clarifications(ambiguity_data):
            with show_loading_message("❓ Generating clarification questions..."):
                questions = ambiguity_detector.generate_clarification_questions(
                    user_input,
                    ambiguity_data
                )
                st.session_state.clarification_questions = questions
                st.session_state.current_stage = "clarification"
        else:
            # Skip to planning
            st.session_state.current_stage = "planning"
            generate_plan(user_input)
        
        # Add to history
        st.session_state.input_history.append(user_input)
        
    except Exception as e:
        show_error(f"Error processing input: {str(e)}")
        st.session_state.current_stage = "input"

def generate_plan(user_input: str):
    """Generate action plan and alternatives."""
    try:
        # Stage 5: Action Plan Generation
        with show_loading_message("📋 Creating your action plan..."):
            plan_data = planner.generate_plan(
                user_input,
                st.session_state.intent_data,
                st.session_state.constraint_data,
                st.session_state.clarification_responses
            )
            st.session_state.plan_data = plan_data
        
        # Stage 6: Alternative Strategies
        with show_loading_message("🔄 Generating alternative strategies..."):
            alternatives = planner.generate_alternatives(
                plan_data,
                st.session_state.constraint_data
            )
            st.session_state.alternatives = alternatives
        
        st.session_state.current_stage = "complete"
        show_success("Analysis complete!")
        
    except Exception as e:
        show_error(f"Error generating plan: {str(e)}")

def main():
    """Main application entry point."""
    # Validate settings
    try:
        settings.validate()
    except ValueError as e:
        st.error(str(e))
        st.info("Please create a .env file with your OPENAI_API_KEY")
        st.stop()
    
    # Initialize session
    initialize_session_state()
    
    # Check if we need to load a session
    if "load_session" in st.session_state:
        load_saved_session(st.session_state.load_session)
        del st.session_state.load_session
    
    # Render sidebar
    render_sidebar()
    
    # Main header with enhanced styling
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎯 IntentOS")
        st.caption("AI Decision Intelligence System - Transform Ambiguity into Action")
    with col2:
        if st.session_state.current_stage == "complete":
            st.success("✅ Analysis Complete")
    
    st.divider()
    
    # Welcome message for first-time users
    if not st.session_state.get("input_history"):
        render_welcome_hero()
        render_stats_banner()
        st.divider()
        render_feature_cards()
        st.divider()
        render_example_prompts()
        st.divider()
        render_how_it_works()
        st.divider()
    
    # Input section
    st.markdown("### What do you want to achieve?")
    st.caption("You don't need to be clear. IntentOS will help you figure it out.")
    
    default_input = st.session_state.pop("example_input", "")
    user_input = st.text_area(
        "Describe your goal:",
        value=default_input,
        height=120,
        placeholder="Example: I want to learn machine learning but I'm not sure where to start...",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        analyze_button = st.button("🚀 Analyze", type="primary")
    with col2:
        if st.button("🔄 Reset"):
            st.session_state.current_stage = "input"
            st.session_state.clarification_responses = {}
            st.rerun()
    
    # Process input
    if analyze_button and user_input.strip():
        st.session_state.current_stage = "processing"
        st.session_state.current_user_input = user_input.strip()
        process_user_input(user_input.strip())
        st.rerun()
    
    st.divider()
    
    # Display results based on current stage
    if st.session_state.current_stage in ["clarification", "planning", "complete"]:
        
        # Stats Dashboard (for complete stage)
        if st.session_state.current_stage == "complete":
            render_stats_dashboard(
                st.session_state.intent_data,
                st.session_state.constraint_data,
                st.session_state.plan_data
            )
            st.divider()
        
        # Create tabs for better organization
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis", "📋 Action Plan", "📈 Visualizations", "💾 Export"])
        
        with tab1:
            # Intent Breakdown
            if st.session_state.intent_data:
                col1, col2 = st.columns([2, 1])
                with col1:
                    render_intent_breakdown(st.session_state.intent_data)
                with col2:
                    render_confidence_gauge(
                        st.session_state.intent_data.get("confidence_score", 0.5),
                        "Intent Confidence"
                    )
                st.divider()
            
            # Constraint Analysis
            if st.session_state.constraint_data:
                col1, col2 = st.columns([2, 1])
                with col1:
                    render_constraint_analysis(st.session_state.constraint_data)
                with col2:
                    render_constraint_radar(st.session_state.constraint_data)
            
            # Clarification Questions
            if st.session_state.current_stage == "clarification":
                st.divider()
                if st.session_state.clarification_questions:
                    responses = render_clarification_questions(
                        st.session_state.clarification_questions
                    )
                    
                    if st.button("✅ Submit Answers", type="primary"):
                        st.session_state.clarification_responses = responses
                        st.session_state.current_stage = "planning"
                        generate_plan(user_input)
                        st.rerun()
        
        with tab2:
            # Action Plan
            if st.session_state.current_stage == "complete":
                if st.session_state.plan_data:
                    render_action_plan(st.session_state.plan_data)
                    st.divider()
                    
                    # Progress Tracker
                    render_progress_tracker(st.session_state.plan_data)
                    st.divider()
                
                # Alternative Strategies
                if st.session_state.alternatives:
                    render_alternative_strategies(st.session_state.alternatives)
            else:
                st.info("Complete the analysis to see your action plan.")
        
        with tab3:
            # Visualizations
            if st.session_state.current_stage == "complete" and st.session_state.plan_data:
                render_timeline_visualization(st.session_state.plan_data)
            else:
                st.info("Complete the analysis to see visualizations.")
        
        with tab4:
            # Export Options
            if st.session_state.current_stage == "complete":
                render_export_options(
                    st.session_state.plan_data,
                    st.session_state.intent_data,
                    st.session_state.constraint_data
                )
                
                st.divider()
                
                # Save session
                st.subheader("💾 Save Session")
                st.caption("Save this analysis to load later")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    session_name = st.text_input(
                        "Session name (optional)",
                        placeholder="my_project",
                        label_visibility="collapsed"
                    )
                with col2:
                    if st.button("💾 Save", type="primary", use_container_width=True):
                        try:
                            filepath = session_manager.save_session(
                                intent_data=st.session_state.intent_data,
                                constraint_data=st.session_state.constraint_data,
                                plan_data=st.session_state.plan_data,
                                user_input=st.session_state.current_user_input,
                                alternatives=st.session_state.alternatives,
                                session_name=session_name if session_name else None
                            )
                            st.success(f"✅ Session saved!")
                        except Exception as e:
                            st.error(f"Failed to save: {str(e)}")
            else:
                st.info("Complete the analysis to export your plan.")

if __name__ == "__main__":
    main()
