"""Reusable UI components for IntentOS."""
import streamlit as st
from typing import Dict, Any, List

def render_sidebar():
    """Render the left sidebar with app info and controls."""
    with st.sidebar:
        st.title("🎯 IntentOS")
        st.caption("AI Decision Intelligence")
        
        st.divider()
        
        # Quick Stats
        st.markdown("### 📊 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Analyses", len(st.session_state.get("input_history", [])))
        with col2:
            stage = st.session_state.get("current_stage", "input")
            stage_emoji = {
                "input": "⏳",
                "processing": "⚙️",
                "clarification": "❓",
                "planning": "📋",
                "complete": "✅"
            }
            st.metric("Stage", stage_emoji.get(stage, "⏳"))
        
        st.divider()
        
        # Settings
        st.markdown("### ⚙️ Settings")
        
        # Session memory toggle
        use_memory = st.toggle(
            "Session Memory",
            value=st.session_state.get("use_memory", True),
            help="Maintain context across interactions"
        )
        st.session_state.use_memory = use_memory
        
        # Confidence threshold
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.get("confidence_threshold", 0.6),
            step=0.05,
            help="Minimum confidence before asking clarifications"
        )
        st.session_state.confidence_threshold = confidence_threshold
        
        # Max clarification questions
        max_questions = st.slider(
            "Max Questions",
            min_value=1,
            max_value=5,
            value=3,
            help="Maximum clarification questions to ask"
        )
        st.session_state.max_questions = max_questions
        
        st.divider()
        
        # Input history
        if "input_history" in st.session_state and st.session_state.input_history:
            st.markdown("### 📝 Recent Inputs")
            for i, hist_input in enumerate(reversed(st.session_state.input_history[-5:])):
                with st.expander(f"#{len(st.session_state.input_history) - i}", expanded=False):
                    st.text(hist_input[:100] + ("..." if len(hist_input) > 100 else ""))
        
        st.divider()
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.current_stage = "input"
                st.session_state.clarification_responses = {}
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear All", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key not in ["use_memory", "confidence_threshold", "max_questions"]:
                        del st.session_state[key]
                st.rerun()
        
        st.divider()
        
        # Saved Sessions
        st.markdown("### 💾 Saved Sessions")
        try:
            from utils.session_manager import session_manager
            
            sessions = session_manager.list_sessions()
            
            if sessions:
                for session in sessions[:3]:  # Show last 3
                    with st.expander(f"📄 {session['timestamp'][:10]}", expanded=False):
                        st.caption(session['user_input'][:80] + "...")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("📂 Load", key=f"load_{session['filename']}", use_container_width=True):
                                st.session_state.load_session = session['filename']
                                st.rerun()
                        with col2:
                            if st.button("🗑️ Del", key=f"del_{session['filename']}", use_container_width=True):
                                session_manager.delete_session(session['filename'])
                                st.rerun()
            else:
                st.caption("No saved sessions yet")
        except Exception as e:
            st.caption("Session management unavailable")
        
        st.divider()
        
        # About section
        with st.expander("ℹ️ About IntentOS"):
            st.markdown("""
            **IntentOS** is an AI-powered decision intelligence system that:
            
            - 🎯 Extracts intent from ambiguous input
            - ⚙️ Identifies constraints and context
            - ❓ Asks smart clarification questions
            - 📋 Generates actionable plans
            - 🔄 Provides alternative strategies
            
            Built with GPT-4 and Streamlit.
            """)

def render_intent_breakdown(intent_data: Dict[str, Any]):
    """Render intent analysis section."""
    st.subheader("🎯 Intent Breakdown")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Primary intent
        st.markdown(f"**Primary Intent:** {intent_data.get('primary_intent', 'Unknown')}")
        
        # Secondary intents
        secondary = intent_data.get("secondary_intents", [])
        if secondary:
            st.markdown("**Secondary Intents:**")
            for intent in secondary:
                st.markdown(f"- {intent}")
        
        # Category
        category = intent_data.get("intent_category", "general")
        st.markdown(f"**Category:** `{category}`")
    
    with col2:
        # Confidence meter
        confidence = intent_data.get("confidence_score", 0.5)
        st.metric("Confidence", f"{confidence:.0%}")
        st.progress(confidence)
    
    # Reasoning
    if intent_data.get("reasoning"):
        with st.expander("Analysis Details"):
            st.info(intent_data["reasoning"])

def render_constraint_analysis(constraint_data: Dict[str, Any]):
    """Render constraint analysis section."""
    st.subheader("⚙️ Constraint Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Time constraint
        time_constraint = constraint_data.get("time_constraint", {})
        time_value = time_constraint.get("value")
        urgency = time_constraint.get("urgency")
        
        if time_value:
            st.markdown(f"**Time:** {time_value}")
            if urgency:
                urgency_colors = {
                    "low": "🟢",
                    "medium": "🟡",
                    "high": "🟠",
                    "critical": "🔴"
                }
                st.markdown(f"**Urgency:** {urgency_colors.get(urgency, '')} {urgency.title()}")
        else:
            st.markdown("**Time:** _Not specified_")
        
        # Skill level
        skill = constraint_data.get("skill_level")
        if skill:
            st.markdown(f"**Skill Level:** {skill.title()}")
        else:
            st.markdown("**Skill Level:** _Not specified_")
    
    with col2:
        # Resources
        resources = constraint_data.get("resources", {})
        
        if resources.get("budget"):
            st.markdown(f"**Budget:** {resources['budget']}")
        
        if resources.get("tools"):
            st.markdown("**Tools:**")
            for tool in resources["tools"]:
                st.markdown(f"- {tool}")
        
        if resources.get("team_size"):
            st.markdown(f"**Team Size:** {resources['team_size']}")
    
    # Preferences
    preferences = constraint_data.get("preferences", [])
    if preferences:
        st.markdown("**Preferences:**")
        cols = st.columns(min(len(preferences), 3))
        for i, pref in enumerate(preferences):
            with cols[i % len(cols)]:
                st.markdown(f"🔹 {pref}")
    
    # Context
    context = constraint_data.get("context")
    if context:
        with st.expander("Additional Context"):
            st.write(context)

def render_clarification_questions(questions: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Render clarification questions and collect responses.
    
    Returns:
        Dictionary of question -> response
    """
    st.subheader("❓ Clarification Questions")
    st.caption("Help us understand your needs better")
    
    responses = {}
    
    for i, q in enumerate(questions):
        impact = q.get("impact", "medium")
        impact_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(impact, "⚪")
        
        with st.container():
            st.markdown(f"{impact_emoji} **Question {i+1}:** {q['question']}")
            
            if q.get("reason"):
                st.caption(f"_{q['reason']}_")
            
            response = st.text_input(
                "Your answer:",
                key=f"clarification_{i}",
                placeholder="Type your response..."
            )
            
            if response:
                responses[q["question"]] = response
            
            st.divider()
    
    return responses

def render_action_plan(plan_data: Dict[str, Any]):
    """Render the action plan in timeline format."""
    st.subheader("📋 Action Plan")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Steps", len(plan_data.get("plan", [])))
    with col2:
        st.metric("Estimated Time", plan_data.get("total_estimated_time", "Unknown"))
    with col3:
        critical_count = len(plan_data.get("critical_path", []))
        st.metric("Critical Steps", critical_count)
    
    st.divider()
    
    # Steps
    steps = plan_data.get("plan", [])
    critical_path = set(plan_data.get("critical_path", []))
    
    for step in steps:
        step_num = step.get("step_number", 0)
        is_critical = step_num in critical_path
        
        # Step header
        icon = "⭐" if is_critical else "📌"
        title = step.get("title", f"Step {step_num}")
        
        with st.expander(f"{icon} **Step {step_num}: {title}**", expanded=False):
            st.markdown(step.get("description", ""))
            
            col1, col2 = st.columns(2)
            
            with col1:
                if step.get("estimated_time"):
                    st.markdown(f"⏱️ **Time:** {step['estimated_time']}")
                
                if step.get("dependencies"):
                    deps = ", ".join(map(str, step["dependencies"]))
                    st.markdown(f"🔗 **Depends on:** Steps {deps}")
            
            with col2:
                if step.get("resources_needed"):
                    st.markdown("🛠️ **Resources:**")
                    for resource in step["resources_needed"]:
                        st.markdown(f"- {resource}")
            
            if step.get("success_criteria"):
                st.success(f"✅ Success: {step['success_criteria']}")
    
    # Risks
    risks = plan_data.get("risks", [])
    if risks:
        st.divider()
        st.markdown("⚠️ **Potential Risks:**")
        for risk in risks:
            st.warning(risk)
    
    # Success metrics
    metrics = plan_data.get("success_metrics", [])
    if metrics:
        st.divider()
        st.markdown("🎯 **Success Metrics:**")
        for metric in metrics:
            st.info(metric)

def render_alternative_strategies(alternatives: List[Dict[str, Any]]):
    """Render alternative strategies section."""
    st.subheader("🔄 Alternative Strategies")
    
    for alt in alternatives:
        scenario = alt.get("scenario", "Alternative")
        
        with st.expander(f"💡 {scenario.title()}"):
            st.markdown(f"**Strategy:** {alt.get('strategy', '')}")
            
            if alt.get("key_changes"):
                st.markdown("**Key Changes:**")
                for change in alt["key_changes"]:
                    st.markdown(f"- {change}")
            
            if alt.get("tradeoffs"):
                st.markdown(f"**Tradeoffs:** {alt['tradeoffs']}")

def show_loading_message(message: str):
    """Display a loading message."""
    return st.spinner(message)

def show_error(message: str):
    """Display an error message."""
    st.error(f"❌ {message}")

def show_success(message: str):
    """Display a success message."""
    st.success(f"✅ {message}")
