"""Advanced UI components with enhanced visualizations."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List
import json
from datetime import datetime

def render_progress_tracker(plan_data: Dict[str, Any]):
    """Render an interactive progress tracker for the action plan."""
    st.subheader("📊 Plan Progress Tracker")
    
    steps = plan_data.get("plan", [])
    if not steps:
        return
    
    # Create progress visualization
    completed = st.session_state.get("completed_steps", set())
    
    progress_pct = len(completed) / len(steps) * 100 if steps else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Steps", len(steps))
    with col2:
        st.metric("Completed", len(completed))
    with col3:
        st.metric("Progress", f"{progress_pct:.0f}%")
    
    st.progress(progress_pct / 100)
    
    # Interactive checklist
    st.markdown("### ✅ Step Checklist")
    for step in steps:
        step_num = step.get("step_number", 0)
        title = step.get("title", f"Step {step_num}")
        
        is_completed = step_num in completed
        
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            if st.checkbox("", value=is_completed, key=f"step_check_{step_num}"):
                completed.add(step_num)
            else:
                completed.discard(step_num)
        with col2:
            st.markdown(f"**Step {step_num}:** {title}")
    
    st.session_state.completed_steps = completed

def render_timeline_visualization(plan_data: Dict[str, Any]):
    """Render a Gantt-style timeline visualization."""
    st.subheader("📅 Timeline Visualization")
    
    steps = plan_data.get("plan", [])
    if not steps:
        return
    
    # Create timeline data
    fig = go.Figure()
    
    for i, step in enumerate(steps):
        step_num = step.get("step_number", i + 1)
        title = step.get("title", f"Step {step_num}")
        
        # Estimate duration (simplified)
        time_str = step.get("estimated_time", "1 day")
        duration = 1  # Default
        
        fig.add_trace(go.Bar(
            name=f"Step {step_num}",
            x=[duration],
            y=[title],
            orientation='h',
            text=time_str,
            textposition='inside',
            hovertemplate=f"<b>{title}</b><br>Duration: {time_str}<extra></extra>"
        ))
    
    fig.update_layout(
        barmode='stack',
        showlegend=False,
        height=max(300, len(steps) * 50),
        xaxis_title="Timeline",
        yaxis_title="Steps",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_confidence_gauge(confidence: float, label: str = "Confidence"):
    """Render a gauge chart for confidence scores."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=confidence * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': label, 'font': {'size': 20}},
        delta={'reference': 60, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#ffebee'},
                {'range': [40, 70], 'color': '#fff9c4'},
                {'range': [70, 100], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_constraint_radar(constraint_data: Dict[str, Any]):
    """Render a radar chart showing constraint coverage."""
    st.subheader("🎯 Constraint Coverage")
    
    # Define constraint categories
    categories = ['Time', 'Skills', 'Resources', 'Budget', 'Team']
    
    # Calculate scores (0-1) for each category
    scores = []
    
    # Time
    time_val = constraint_data.get("time_constraint", {}).get("value")
    scores.append(1.0 if time_val else 0.0)
    
    # Skills
    skill = constraint_data.get("skill_level")
    scores.append(1.0 if skill else 0.0)
    
    # Resources
    resources = constraint_data.get("resources", {})
    tools = resources.get("tools", [])
    scores.append(min(1.0, len(tools) / 3) if tools else 0.0)
    
    # Budget
    budget = resources.get("budget")
    scores.append(1.0 if budget else 0.0)
    
    # Team
    team = resources.get("team_size")
    scores.append(1.0 if team else 0.0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='Coverage',
        line_color='#4f46e5'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def export_plan_to_json(plan_data: Dict[str, Any], intent_data: Dict[str, Any], 
                        constraint_data: Dict[str, Any]) -> str:
    """Export the complete analysis to JSON."""
    export_data = {
        "timestamp": datetime.now().isoformat(),
        "intent": intent_data,
        "constraints": constraint_data,
        "plan": plan_data,
        "metadata": {
            "app": "IntentOS",
            "version": "2.0"
        }
    }
    return json.dumps(export_data, indent=2)

def export_plan_to_markdown(plan_data: Dict[str, Any], intent_data: Dict[str, Any],
                           constraint_data: Dict[str, Any]) -> str:
    """Export the plan to Markdown format."""
    md = f"""# IntentOS Action Plan
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 🎯 Intent
**Primary Goal:** {intent_data.get('primary_intent', 'N/A')}

**Confidence:** {intent_data.get('confidence_score', 0) * 100:.0f}%

"""
    
    # Add secondary intents
    secondary = intent_data.get('secondary_intents', [])
    if secondary:
        md += "**Secondary Goals:**\n"
        for intent in secondary:
            md += f"- {intent}\n"
        md += "\n"
    
    # Add constraints
    md += "## ⚙️ Constraints\n\n"
    
    time_constraint = constraint_data.get("time_constraint", {})
    if time_constraint.get("value"):
        md += f"**Time:** {time_constraint['value']}\n\n"
    
    skill = constraint_data.get("skill_level")
    if skill:
        md += f"**Skill Level:** {skill}\n\n"
    
    # Add action plan
    md += "## 📋 Action Plan\n\n"
    
    steps = plan_data.get("plan", [])
    for step in steps:
        step_num = step.get("step_number", 0)
        title = step.get("title", f"Step {step_num}")
        desc = step.get("description", "")
        time = step.get("estimated_time", "")
        
        md += f"### Step {step_num}: {title}\n\n"
        md += f"{desc}\n\n"
        if time:
            md += f"**Estimated Time:** {time}\n\n"
        
        resources = step.get("resources_needed", [])
        if resources:
            md += "**Resources:**\n"
            for resource in resources:
                md += f"- {resource}\n"
            md += "\n"
    
    # Add risks
    risks = plan_data.get("risks", [])
    if risks:
        md += "## ⚠️ Risks\n\n"
        for risk in risks:
            md += f"- {risk}\n"
        md += "\n"
    
    return md

def render_export_options(plan_data: Dict[str, Any], intent_data: Dict[str, Any],
                          constraint_data: Dict[str, Any]):
    """Render export options for the plan."""
    st.subheader("💾 Export Plan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON export
        json_data = export_plan_to_json(plan_data, intent_data, constraint_data)
        st.download_button(
            label="📄 Download as JSON",
            data=json_data,
            file_name=f"intentos_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # Markdown export
        md_data = export_plan_to_markdown(plan_data, intent_data, constraint_data)
        st.download_button(
            label="📝 Download as Markdown",
            data=md_data,
            file_name=f"intentos_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )

def render_stats_dashboard(intent_data: Dict[str, Any], constraint_data: Dict[str, Any],
                           plan_data: Dict[str, Any]):
    """Render a comprehensive stats dashboard."""
    st.subheader("📈 Analysis Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        confidence = intent_data.get("confidence_score", 0)
        st.metric(
            "Intent Confidence",
            f"{confidence * 100:.0f}%",
            delta=f"{(confidence - 0.6) * 100:.0f}%" if confidence > 0.6 else None
        )
    
    with col2:
        steps_count = len(plan_data.get("plan", []))
        st.metric("Total Steps", steps_count)
    
    with col3:
        risks_count = len(plan_data.get("risks", []))
        st.metric("Identified Risks", risks_count)
    
    with col4:
        time_est = plan_data.get("total_estimated_time", "N/A")
        st.metric("Est. Duration", time_est)
