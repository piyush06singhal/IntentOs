"""Advanced UI components for elite features."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List

def render_multi_intent_analysis(multi_intent_data: Dict[str, Any]):
    """Render multi-intent decomposition with conflict visualization."""
    st.subheader("🎯 Multi-Intent Analysis")
    
    if not multi_intent_data.get("has_multiple_intents"):
        st.success("✅ Single, clear intent detected")
        return
    
    intents = multi_intent_data.get("intents", [])
    conflicts = multi_intent_data.get("conflicts", [])
    
    # Complexity score
    complexity = multi_intent_data.get("total_complexity_score", 0.5)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Detected Intents", len(intents))
    with col2:
        st.metric("Conflicts Found", len(conflicts))
    with col3:
        st.metric("Complexity", f"{complexity:.0%}", 
                 delta="High" if complexity > 0.7 else "Moderate" if complexity > 0.4 else "Low")
    
    st.divider()
    
    # Intent breakdown
    st.markdown("### 📋 Detected Intents")
    for i, intent in enumerate(intents):
        priority_colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        priority_emoji = priority_colors.get(intent.get("priority", "medium"), "⚪")
        
        with st.expander(f"{priority_emoji} Intent {i+1}: {intent.get('intent', 'Unknown')}", expanded=i==0):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Priority:** {intent.get('priority', 'medium').title()}")
                st.markdown(f"**Effort:** {intent.get('estimated_effort', 'Unknown')}")
            with col2:
                deps = intent.get("dependencies", [])
                if deps:
                    st.markdown(f"**Dependencies:** Intents {', '.join(map(str, deps))}")
                else:
                    st.markdown("**Dependencies:** None")
    
    # Conflict visualization
    if conflicts:
        st.divider()
        st.markdown("### ⚠️ Detected Conflicts")
        
        for conflict in conflicts:
            severity = conflict.get("severity", "medium")
            severity_colors = {
                "high": "#ef4444",
                "medium": "#f59e0b",
                "low": "#10b981"
            }
            color = severity_colors.get(severity, "#6b7280")
            
            st.markdown(f"""
            <div style='background-color: {color}22; border-left: 4px solid {color}; 
                        padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                <strong style='color: {color};'>{conflict.get('type', 'Unknown').upper()} CONFLICT</strong>
                <p style='margin: 0.5rem 0 0 0;'>{conflict.get('description', '')}</p>
                <small>Affects: Intents {', '.join(map(str, conflict.get('affected_intents', [])))}</small>
            </div>
            """, unsafe_allow_html=True)

def render_conflict_resolution(resolution_data: Dict[str, Any]):
    """Render conflict resolution strategies."""
    st.subheader("🔧 Conflict Resolution")
    
    resolutions = resolution_data.get("resolutions", [])
    
    if not resolutions:
        st.info("No conflicts to resolve")
        return
    
    # Overall recommendation
    st.markdown(f"**Recommended Approach:** {resolution_data.get('recommended_approach', 'N/A')}")
    
    risk_level = resolution_data.get("risk_level", "medium")
    risk_colors = {"low": "🟢", "medium": "🟡", "high": "🔴"}
    st.markdown(f"**Risk Level:** {risk_colors.get(risk_level, '⚪')} {risk_level.title()}")
    
    st.divider()
    
    # Resolution strategies
    for i, resolution in enumerate(resolutions):
        strategy = resolution.get("strategy", "unknown")
        confidence = resolution.get("confidence", 0.5)
        
        with st.expander(f"Strategy {i+1}: {strategy.title()}", expanded=i==0):
            st.markdown(f"**Rationale:** {resolution.get('rationale', '')}")
            st.markdown(f"**Confidence:** {confidence:.0%}")
            
            st.progress(confidence)
            
            if resolution.get("execution_order"):
                st.markdown("**Execution Order:**")
                for idx, step in enumerate(resolution.get("execution_order", [])):
                    st.markdown(f"{idx+1}. Intent {step}")
            
            if resolution.get("tradeoffs"):
                st.info(f"**Tradeoffs:** {resolution['tradeoffs']}")

def render_confidence_dashboard(confidence_data: Dict[str, Any]):
    """Render confidence assessment dashboard."""
    st.subheader("📊 Confidence Assessment")
    
    overall = confidence_data.get("overall_confidence", 0.5)
    
    # Overall confidence gauge
    col1, col2 = st.columns([1, 2])
    
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Confidence"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 40], 'color': "#fee2e2"},
                    {'range': [40, 70], 'color': "#fef3c7"},
                    {'range': [70, 100], 'color': "#d1fae5"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Aspect scores
        aspect_scores = confidence_data.get("aspect_scores", {})
        
        if aspect_scores:
            aspects = []
            scores = []
            
            for aspect, data in aspect_scores.items():
                aspects.append(aspect.replace("_", " ").title())
                scores.append(data.get("score", 0.5) * 100)
            
            fig = go.Figure(go.Bar(
                x=scores,
                y=aspects,
                orientation='h',
                marker=dict(
                    color=scores,
                    colorscale='RdYlGn',
                    showscale=False
                ),
                text=[f"{s:.0f}%" for s in scores],
                textposition='auto'
            ))
            
            fig.update_layout(
                height=250,
                xaxis_title="Confidence %",
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(range=[0, 100])
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Low confidence areas
    low_conf = confidence_data.get("low_confidence_areas", [])
    critical_gaps = confidence_data.get("critical_gaps", [])
    
    if critical_gaps:
        st.warning(f"**Critical Gaps:** {', '.join(critical_gaps)}")
    
    if low_conf:
        st.info(f"**Low Confidence Areas:** {', '.join(low_conf)}")

def render_plan_comparison(plans: List[Dict[str, Any]], scored_plans: List[Dict[str, Any]]):
    """Render plan comparison matrix."""
    st.subheader("📊 Plan Comparison")
    
    if not plans or not scored_plans:
        st.info("No plans to compare")
        return
    
    # Create comparison table
    strategies = []
    times = []
    costs = []
    success_probs = []
    scores = []
    
    for plan, scored in zip(plans, scored_plans):
        strategies.append(plan.get("strategy", "Unknown"))
        times.append(plan.get("total_time", "N/A"))
        costs.append(plan.get("total_cost", "N/A"))
        success_probs.append(plan.get("success_probability", 0.5) * 100)
        scores.append(scored.get("overall_score", 0.5) * 100)
    
    # Radar chart comparison
    fig = go.Figure()
    
    categories = ['Time Feasibility', 'Resource Feasibility', 'Skill Match', 
                  'Risk Acceptability', 'Success Probability', 'Priority Alignment']
    
    for i, scored in enumerate(scored_plans):
        scores_dict = scored.get("scores", {})
        values = [
            scores_dict.get("time_feasibility", 0.5) * 100,
            scores_dict.get("resource_feasibility", 0.5) * 100,
            scores_dict.get("skill_match", 0.5) * 100,
            scores_dict.get("risk_acceptability", 0.5) * 100,
            scores_dict.get("success_probability", 0.5) * 100,
            scores_dict.get("priority_alignment", 0.5) * 100
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=strategies[i]
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed comparison table
    st.markdown("### 📋 Detailed Comparison")
    
    comparison_data = {
        "Strategy": strategies,
        "Time": times,
        "Cost": costs,
        "Success %": [f"{p:.0f}%" for p in success_probs],
        "Overall Score": [f"{s:.0f}%" for s in scores]
    }
    
    st.table(comparison_data)
    
    # Recommendations
    st.divider()
    st.markdown("### 💡 Recommendations")
    
    for i, scored in enumerate(scored_plans):
        recommendation = scored.get("recommendation", "acceptable")
        reasoning = scored.get("reasoning", "")
        
        if recommendation == "highly recommended":
            st.success(f"✅ **{strategies[i]}**: {reasoning}")
        elif recommendation == "recommended":
            st.info(f"ℹ️ **{strategies[i]}**: {reasoning}")
        elif recommendation == "acceptable":
            st.warning(f"⚠️ **{strategies[i]}**: {reasoning}")
        else:
            st.error(f"❌ **{strategies[i]}**: {reasoning}")

def render_intent_history(history: List[Dict[str, Any]]):
    """Render intent history timeline."""
    st.subheader("📜 Intent History")
    
    if not history:
        st.info("No previous sessions found")
        return
    
    for i, entry in enumerate(history):
        timestamp = entry.get("timestamp", "Unknown")
        intent = entry.get("intent", {})
        primary = intent.get("primary_intent", "Unknown goal")
        
        with st.expander(f"Session {len(history)-i}: {timestamp[:10]}", expanded=i==0):
            st.markdown(f"**Goal:** {primary}")
            st.markdown(f"**Time:** {timestamp}")
            
            if intent.get("confidence_score"):
                st.progress(intent["confidence_score"])

def render_drift_analysis(drift_data: Dict[str, Any]):
    """Render intent drift analysis."""
    st.subheader("🔄 Intent Drift Analysis")
    
    has_drifted = drift_data.get("has_drifted", False)
    drift_type = drift_data.get("drift_type", "none")
    severity = drift_data.get("drift_severity", 0.0)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if has_drifted:
            st.error("⚠️ Drift Detected")
        else:
            st.success("✅ No Drift")
    
    with col2:
        st.metric("Drift Type", drift_type.title())
    
    with col3:
        st.metric("Severity", f"{severity:.0%}")
    
    if has_drifted:
        st.divider()
        
        changes = drift_data.get("changes_detected", [])
        if changes:
            st.markdown("### 📝 Detected Changes")
            for change in changes:
                significance = change.get("significance", "medium")
                sig_colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                
                st.markdown(f"""
                {sig_colors.get(significance, '⚪')} **{change.get('aspect', 'Unknown').title()}**  
                From: _{change.get('old_value', 'N/A')}_  
                To: _{change.get('new_value', 'N/A')}_
                """)
        
        st.divider()
        recommendation = drift_data.get("recommendation", "continue")
        reasoning = drift_data.get("reasoning", "")
        
        if recommendation == "restart":
            st.warning(f"**Recommendation:** Start fresh - {reasoning}")
        elif recommendation == "adapt":
            st.info(f"**Recommendation:** Adapt current plan - {reasoning}")
        else:
            st.success(f"**Recommendation:** Continue - {reasoning}")

def render_validation_results(validation: Dict[str, Any]):
    """Render guardrail validation results."""
    st.subheader("🛡️ Validation Results")
    
    is_valid = validation.get("is_valid", True)
    confidence = validation.get("confidence", 1.0)
    issues = validation.get("issues", [])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if is_valid:
            st.success("✅ Valid")
        else:
            st.error("❌ Issues Found")
    
    with col2:
        st.metric("Confidence", f"{confidence:.0%}")
    
    with col3:
        critical_count = validation.get("critical_issues_count", 0)
        st.metric("Critical Issues", critical_count)
    
    if issues:
        st.divider()
        st.markdown("### 🔍 Detected Issues")
        
        for issue in issues:
            severity = issue.get("severity", "medium")
            issue_type = issue.get("type", "unknown")
            
            severity_colors = {
                "critical": "#dc2626",
                "high": "#f59e0b",
                "medium": "#3b82f6",
                "low": "#10b981"
            }
            color = severity_colors.get(severity, "#6b7280")
            
            st.markdown(f"""
            <div style='background-color: {color}22; border-left: 4px solid {color}; 
                        padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                <strong style='color: {color};'>{severity.upper()}: {issue_type.title()}</strong>
                <p style='margin: 0.5rem 0;'>{issue.get('description', '')}</p>
                <small><strong>Location:</strong> {issue.get('location', 'N/A')}</small><br>
                <small><strong>Fix:</strong> {issue.get('suggested_fix', 'N/A')}</small>
            </div>
            """, unsafe_allow_html=True)
        
        if validation.get("was_corrected"):
            st.success(f"✅ Auto-corrected {validation.get('corrections_applied', 0)} issues")
