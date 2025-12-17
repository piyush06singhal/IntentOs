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

# Import advanced engine components
from engine.multi_intent_resolver import multi_intent_resolver
from engine.confidence_engine import confidence_engine
from engine.plan_optimizer import plan_optimizer
from engine.intent_memory import intent_memory
from engine.guardrail_validator import guardrail_validator

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

# Import advanced features UI
from ui.advanced_features_ui import (
    render_multi_intent_analysis,
    render_conflict_resolution,
    render_confidence_dashboard,
    render_plan_comparison,
    render_intent_history,
    render_drift_analysis,
    render_validation_results
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
        background-color: #ffffff;
        border: 3px solid #667eea;
        border-radius: 10px;
        padding: 1rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        color: #1e293b;
    }
    
    .stTextArea>div>div>textarea::placeholder {
        color: #94a3b8;
        font-size: 1rem;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #764ba2;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2);
        background-color: #fefefe;
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
    
    # Advanced features state
    if "multi_intent_data" not in st.session_state:
        st.session_state.multi_intent_data = None
    if "conflict_resolution" not in st.session_state:
        st.session_state.conflict_resolution = None
    if "confidence_assessment" not in st.session_state:
        st.session_state.confidence_assessment = None
    if "multiple_plans" not in st.session_state:
        st.session_state.multiple_plans = []
    if "scored_plans" not in st.session_state:
        st.session_state.scored_plans = []
    if "drift_analysis" not in st.session_state:
        st.session_state.drift_analysis = None
    if "validation_results" not in st.session_state:
        st.session_state.validation_results = None
    if "enable_advanced_features" not in st.session_state:
        st.session_state.enable_advanced_features = False  # Disabled by default for stability

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
    Process user input through the enhanced multi-stage reasoning pipeline.
    
    Pipeline stages:
    1. Multi-Intent Detection & Conflict Resolution
    2. Intent Extraction
    3. Constraint Parsing
    4. Confidence Assessment
    5. Intent Drift Detection (if history exists)
    6. Smart Clarification (confidence-driven)
    7. Multi-Plan Generation & Optimization
    8. Guardrail Validation
    """
    try:
        # Advanced Stage 1: Multi-Intent Detection
        if st.session_state.enable_advanced_features:
            try:
                with show_loading_message("🎯 Detecting multiple intents..."):
                    multi_intent_data = multi_intent_resolver.detect_multiple_intents(user_input)
                    st.session_state.multi_intent_data = multi_intent_data
            except Exception as e:
                st.warning(f"Multi-intent detection skipped: {str(e)}")
                st.session_state.multi_intent_data = None
        
        # Stage 2: Intent Extraction
        with show_loading_message("🔍 Analyzing your intent..."):
            intent_data = intent_engine.extract_intent(user_input)
            st.session_state.intent_data = intent_data
        
        # Stage 3: Constraint Parsing
        with show_loading_message("⚙️ Extracting constraints..."):
            constraint_data = constraint_parser.extract_constraints(user_input)
            st.session_state.constraint_data = constraint_data
        
        # Advanced Stage 4: Confidence Assessment
        if st.session_state.enable_advanced_features:
            try:
                with show_loading_message("📊 Assessing confidence..."):
                    confidence_assessment = confidence_engine.assess_confidence(
                        user_input, intent_data, constraint_data
                    )
                    st.session_state.confidence_assessment = confidence_assessment
            except Exception as e:
                st.warning(f"Confidence assessment skipped: {str(e)}")
                st.session_state.confidence_assessment = None
        
        # Advanced Stage 5: Intent Drift Detection
        if st.session_state.enable_advanced_features and st.session_state.use_memory:
            try:
                with show_loading_message("🔄 Checking intent drift..."):
                    drift_analysis = intent_memory.detect_drift(intent_data)
                    st.session_state.drift_analysis = drift_analysis
            except Exception as e:
                st.warning(f"Drift detection skipped: {str(e)}")
                st.session_state.drift_analysis = None
        
        # Advanced Stage 6: Conflict Resolution (if multiple intents)
        if (st.session_state.enable_advanced_features and 
            st.session_state.multi_intent_data and 
            st.session_state.multi_intent_data.get("has_multiple_intents")):
            
            conflicts = st.session_state.multi_intent_data.get("conflicts", [])
            if conflicts:
                try:
                    with show_loading_message("🔧 Resolving conflicts..."):
                        intents = st.session_state.multi_intent_data.get("intents", [])
                        resolution = multi_intent_resolver.resolve_conflicts(
                            intents, conflicts, constraint_data
                        )
                        st.session_state.conflict_resolution = resolution
                except Exception as e:
                    st.warning(f"Conflict resolution skipped: {str(e)}")
                    st.session_state.conflict_resolution = None
        
        # Stage 7: Smart Clarification (confidence-driven)
        should_clarify = False
        
        if st.session_state.enable_advanced_features and st.session_state.confidence_assessment:
            should_clarify = confidence_engine.should_ask_clarifications(
                st.session_state.confidence_assessment
            )
        else:
            # Fallback to original ambiguity detection
            ambiguity_data = ambiguity_detector.detect_ambiguity(
                user_input, intent_data, constraint_data
            )
            st.session_state.ambiguity_data = ambiguity_data
            should_clarify = ambiguity_detector.should_ask_clarifications(ambiguity_data)
        
        if should_clarify:
            with show_loading_message("❓ Generating smart questions..."):
                if st.session_state.enable_advanced_features:
                    smart_questions = confidence_engine.generate_smart_questions(
                        st.session_state.confidence_assessment,
                        user_input,
                        max_questions=st.session_state.get("max_questions", 3)
                    )
                    st.session_state.clarification_questions = smart_questions.get("questions", [])
                else:
                    questions = ambiguity_detector.generate_clarification_questions(
                        user_input, st.session_state.ambiguity_data
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
    """Generate optimized action plan with validation."""
    try:
        # Advanced Stage 8: Multi-Plan Generation & Optimization
        if st.session_state.enable_advanced_features:
            try:
                with show_loading_message("📋 Generating multiple plan options..."):
                    multiple_plans_data = plan_optimizer.generate_multiple_plans(
                        user_input,
                        st.session_state.intent_data,
                        st.session_state.constraint_data,
                        num_plans=3
                    )
                    st.session_state.multiple_plans = multiple_plans_data.get("plans", [])
                
                with show_loading_message("⚖️ Scoring and optimizing plans..."):
                    scored_plans_data = plan_optimizer.score_plans(
                        st.session_state.multiple_plans,
                        st.session_state.constraint_data
                    )
                    st.session_state.scored_plans = scored_plans_data.get("scored_plans", [])
                    
                    # Select optimal plan
                    optimal_plan_id = scored_plans_data.get("optimal_plan_id")
                    optimal_plan = next(
                        (p for p in st.session_state.multiple_plans if p.get("plan_id") == optimal_plan_id),
                        st.session_state.multiple_plans[0] if st.session_state.multiple_plans else {}
                    )
                    
                    # Convert optimal plan to standard format
                    st.session_state.plan_data = {
                        "plan": optimal_plan.get("steps", []),
                        "total_estimated_time": optimal_plan.get("total_time", "Unknown"),
                        "total_cost": optimal_plan.get("total_cost", "N/A"),
                        "strategy": optimal_plan.get("strategy", "balanced"),
                        "success_probability": optimal_plan.get("success_probability", 0.8),
                        "critical_path": [],
                        "risks": [d for d in optimal_plan.get("key_disadvantages", [])],
                        "success_metrics": [a for a in optimal_plan.get("key_advantages", [])]
                    }
            except Exception as e:
                st.warning(f"Advanced plan optimization failed, using standard planning: {str(e)}")
                # Fallback to standard planning
                with show_loading_message("📋 Creating your action plan..."):
                    plan_data = planner.generate_plan(
                        user_input,
                        st.session_state.intent_data,
                        st.session_state.constraint_data,
                        st.session_state.clarification_responses
                    )
                    st.session_state.plan_data = plan_data
        else:
            # Standard plan generation
            with show_loading_message("📋 Creating your action plan..."):
                plan_data = planner.generate_plan(
                    user_input,
                    st.session_state.intent_data,
                    st.session_state.constraint_data,
                    st.session_state.clarification_responses
                )
                st.session_state.plan_data = plan_data
        
        # Advanced Stage 9: Guardrail Validation
        if st.session_state.enable_advanced_features:
            try:
                with show_loading_message("🛡️ Validating plan..."):
                    validation, corrected_plan = guardrail_validator.validate_and_correct(
                        user_input,
                        st.session_state.constraint_data,
                        st.session_state.plan_data,
                        auto_correct=True
                    )
                    st.session_state.validation_results = validation
                    
                    # Use corrected plan if corrections were made
                    if validation.get("was_corrected"):
                        st.session_state.plan_data = corrected_plan
            except Exception as e:
                st.warning(f"Validation skipped: {str(e)}")
                st.session_state.validation_results = None
        
        # Stage 6: Alternative Strategies
        with show_loading_message("🔄 Generating alternative strategies..."):
            alternatives = planner.generate_alternatives(
                st.session_state.plan_data,
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
    st.markdown("### 💭 What do you want to achieve?")
    st.caption("Type your goal below. You don't need to be clear - IntentOS will help you figure it out.")
    
    default_input = st.session_state.pop("example_input", "")
    user_input = st.text_area(
        "Describe your goal:",
        value=default_input,
        height=150,
        placeholder="Click here and type your goal...\n\nExample: I want to learn machine learning but I'm not sure where to start and I only have 10 hours per week.",
        label_visibility="collapsed",
        key="user_goal_input",
        help="Describe what you want to achieve. Be as detailed or vague as you like!"
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
    if analyze_button:
        if user_input and user_input.strip():
            try:
                st.session_state.current_user_input = user_input.strip()
                process_user_input(user_input.strip())
                # Don't call st.rerun() here - let the page naturally show results
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.exception(e)  # Show full traceback
                st.session_state.current_stage = "input"
        else:
            st.warning("⚠️ Please enter your goal in the text box above before clicking Analyze")
    
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
        if st.session_state.enable_advanced_features:
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📊 Analysis", 
                "🎯 Advanced Analysis",
                "📋 Action Plan", 
                "📈 Visualizations", 
                "🧠 Intelligence",
                "💾 Export"
            ])
        else:
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
        
        # Advanced Features Tabs
        if st.session_state.enable_advanced_features:
            with tab2:
                # Advanced Analysis Tab
                st.markdown("## 🎯 Advanced Intelligence Analysis")
                
                # Multi-Intent Analysis
                if st.session_state.multi_intent_data:
                    render_multi_intent_analysis(st.session_state.multi_intent_data)
                    st.divider()
                
                # Conflict Resolution
                if st.session_state.conflict_resolution:
                    render_conflict_resolution(st.session_state.conflict_resolution)
                    st.divider()
                
                # Confidence Assessment
                if st.session_state.confidence_assessment:
                    render_confidence_dashboard(st.session_state.confidence_assessment)
                else:
                    st.info("Advanced analysis will appear here after processing your input.")
            
            with tab5:
                # Intelligence Tab
                st.markdown("## 🧠 AI Intelligence Features")
                
                # Plan Comparison
                if st.session_state.multiple_plans and st.session_state.scored_plans:
                    render_plan_comparison(
                        st.session_state.multiple_plans,
                        st.session_state.scored_plans
                    )
                    st.divider()
                
                # Intent Drift Analysis
                if st.session_state.drift_analysis:
                    render_drift_analysis(st.session_state.drift_analysis)
                    st.divider()
                
                # Intent History
                if st.session_state.use_memory:
                    history = intent_memory.get_intent_history(limit=5)
                    if history:
                        render_intent_history(history)
                    st.divider()
                
                # Validation Results
                if st.session_state.validation_results:
                    render_validation_results(st.session_state.validation_results)
                
                if not any([
                    st.session_state.multiple_plans,
                    st.session_state.drift_analysis,
                    st.session_state.validation_results
                ]):
                    st.info("Intelligence features will appear here after analysis.")
            
            with tab6:
                # Export tab (same as tab4 in non-advanced mode)
                if st.session_state.current_stage == "complete":
                    render_export_options(
                        st.session_state.plan_data,
                        st.session_state.intent_data,
                        st.session_state.constraint_data
                    )
                    
                    st.divider()
                    
                    # Save session with memory
                    st.subheader("💾 Save Session")
                    st.caption("Save this analysis to load later")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        session_name = st.text_input(
                            "Session name (optional)",
                            placeholder="my_project",
                            label_visibility="collapsed",
                            key="advanced_session_name"
                        )
                    with col2:
                        if st.button("💾 Save", type="primary", use_container_width=True, key="advanced_save"):
                            try:
                                # Save to session manager
                                filepath = session_manager.save_session(
                                    intent_data=st.session_state.intent_data,
                                    constraint_data=st.session_state.constraint_data,
                                    plan_data=st.session_state.plan_data,
                                    user_input=st.session_state.current_user_input,
                                    alternatives=st.session_state.alternatives,
                                    session_name=session_name if session_name else None
                                )
                                
                                # Save to intent memory
                                if st.session_state.use_memory:
                                    intent_memory.save_intent(
                                        st.session_state.intent_data,
                                        st.session_state.constraint_data,
                                        st.session_state.plan_data
                                    )
                                
                                st.success(f"✅ Session saved with memory!")
                            except Exception as e:
                                st.error(f"Failed to save: {str(e)}")
                else:
                    st.info("Complete the analysis to export your plan.")

if __name__ == "__main__":
    main()
