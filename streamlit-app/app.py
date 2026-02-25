import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
from pathlib import Path
import yaml
import os

from config import (
    APP_TITLE, APP_ICON, RUBRICS_DIR, TECHNIQUES_DIR, OPENROUTER_API_KEY, CSS_FILE

)
import config
from datetime import datetime
from pathlib import Path
from utils.llm_client import LLMClient
from utils.rubric_builder import RubricBuilder
from utils.prompt_analyzer import PromptAnalyzer
from utils.evaluator import Evaluator
from utils.report_generator import ReportGenerator
from utils.auto_evaluator import AutoEvaluator

# Set page config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Utils
rubric_builder = RubricBuilder(config.RUBRICS_DIR)
prompt_analyzer = PromptAnalyzer(config.TECHNIQUES_DIR)
evaluator = Evaluator()

# Session State Initialization
if "responses" not in st.session_state:
    st.session_state.responses = []
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""
if "selected_rubric" not in st.session_state:
    st.session_state.selected_rubric = None
if "model_a" not in st.session_state:
    st.session_state.model_a = None
if "model_b" not in st.session_state:
    st.session_state.model_b = None
if "params_a" not in st.session_state:
    st.session_state.params_a = {"temperature": 0.7, "top_p": 1.0, "max_tokens": 4096, "top_k": None}
if "params_b" not in st.session_state:
    st.session_state.params_b = {"temperature": 1.0, "top_p": 1.0, "max_tokens": 4096, "top_k": None}
if "user_justification" not in st.session_state:
    st.session_state.user_justification = ""
if "preferred_response" not in st.session_state:
    st.session_state.preferred_response = "A"
if "report_model" not in st.session_state:
    st.session_state.report_model = None
if "evaluation_complete" not in st.session_state:
    st.session_state.evaluation_complete = False
if "final_scores" not in st.session_state:
    st.session_state.final_scores = {"a": 0.0, "b": 0.0}
if "eval_mode" not in st.session_state:
    st.session_state.eval_mode = "Manual Evaluation"
if "auto_eval_data" not in st.session_state:
    st.session_state.auto_eval_data = None

def main():
    # Inject Custom CSS
    if CSS_FILE.exists():
        with open(CSS_FILE, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.title(f"{APP_ICON} {APP_TITLE}")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Generate & Evaluate", "Prompt Analysis", "Rubric Builder"])
    
    # API Key Handling
    api_key = st.sidebar.text_input("OpenRouter API Key", type="password", value=OPENROUTER_API_KEY)
    if api_key:
        llm_client = LLMClient(api_key=api_key)
    else:
        st.sidebar.warning("Please enter your OpenRouter API Key to use AI features.")
        llm_client = None

    if page == "Generate & Evaluate":
        render_generate_page(llm_client)
    elif page == "Prompt Analysis":
        render_prompt_analysis_page(prompt_analyzer, llm_client)
    elif page == "Rubric Builder":
        render_rubric_builder(rubric_builder)

def render_generate_page(llm_client):
    st.header("1. Generate Responses")
    
    # Prompt input
    prompt = st.text_area("Enter your prompt:", height=150, value=st.session_state.current_prompt)
    st.session_state.current_prompt = prompt
    
    # Model selection mode
    comparison_mode = st.radio(
        "Comparison Mode",
        ["Same Model (Varied Parameters)", "Different Models"],
        help="Choose to compare responses from the same model with different parameters, or from two different models"
    )
    
    # Fetch free models
    if llm_client:
        free_models = llm_client.get_free_models()
        model_options = [f"{m['name']} ({m['id']})" for m in free_models]
        model_ids = {f"{m['name']} ({m['id']})": m['id'] for m in free_models}
        
        if not model_options:
            st.warning("No free models available. Please check your API key or try again later.")
            return
    else:
        st.warning("Please enter your OpenRouter API key in the sidebar.")
        return
    
    # Model selection based on mode
    col1, col2 = st.columns(2)
    
    if comparison_mode == "Same Model (Varied Parameters)":
        with col1:
            selected_model = st.selectbox("Select Model", model_options, key="model_same")
            model_a_id = model_ids[selected_model]
            model_b_id = model_a_id
            st.session_state.model_a = model_a_id
            st.session_state.model_b = model_b_id
    else:
        with col1:
            selected_model_a = st.selectbox("Select Model A", model_options, key="model_a_diff")
            model_a_id = model_ids[selected_model_a]
            st.session_state.model_a = model_a_id
        with col2:
            selected_model_b = st.selectbox("Select Model B", model_options, key="model_b_diff")
            model_b_id = model_ids[selected_model_b]
            st.session_state.model_b = model_b_id
    
    # Advanced Parameters Section
    with st.expander("⚙️ Advanced Parameters", expanded=False):
        st.markdown("### Configure generation parameters for each response")
        
        param_col1, param_col2 = st.columns(2)
        
        with param_col1:
            st.markdown("**Response A Parameters**")
            temp_a = st.slider("Temperature A", 0.0, 2.0, st.session_state.params_a["temperature"], 0.1, 
                               help="Temperature controls the randomness of the model's output. A higher value (e.g., 1.5) makes the output more creative and diverse, while a lower value (e.g., 0.2) makes it more focused, predictable, and deterministic.")
            top_p_a = st.slider("Top P A", 0.0, 1.0, st.session_state.params_a["top_p"], 0.05,
                               help="Top-p (nucleus sampling) limits the model's vocabulary choice to the tokens that comprise the top 'p' probability mass. A lower value (e.g., 0.5) restricts choices to only the most likely words, making output safer. 1.0 uses all words.")
            max_tokens_a = st.number_input("Max Tokens A", 100, 32000, st.session_state.params_a["max_tokens"], 100,
                                          help="The maximum number of tokens (words or word pieces) the model is allowed to generate in its response. Setting this limits the length of the output, preventing overly long responses.")
            top_k_a = st.number_input("Top K A (optional)", 0, 100, st.session_state.params_a["top_k"] or 0, 1,
                                     help="Top-k sampling limits the model to select its next word from only the 'k' most likely next words. This helps prevent the model from choosing highly improbable words, maintaining output quality. 0 disables it.")
            
            st.session_state.params_a = {
                "temperature": temp_a,
                "top_p": top_p_a,
                "max_tokens": max_tokens_a,
                "top_k": top_k_a if top_k_a > 0 else None
            }
        
        with param_col2:
            st.markdown("**Response B Parameters**")
            temp_b = st.slider("Temperature B", 0.0, 2.0, st.session_state.params_b["temperature"], 0.1,
                               help="Temperature controls the randomness of the model's output. A higher value (e.g., 1.5) makes the output more creative and diverse, while a lower value (e.g., 0.2) makes it more focused, predictable, and deterministic.")
            top_p_b = st.slider("Top P B", 0.0, 1.0, st.session_state.params_b["top_p"], 0.05,
                               help="Top-p (nucleus sampling) limits the model's vocabulary choice to the tokens that comprise the top 'p' probability mass. A lower value (e.g., 0.5) restricts choices to only the most likely words, making output safer. 1.0 uses all words.")
            max_tokens_b = st.number_input("Max Tokens B", 100, 32000, st.session_state.params_b["max_tokens"], 100,
                                          help="The maximum number of tokens (words or word pieces) the model is allowed to generate in its response. Setting this limits the length of the output, preventing overly long responses.")
            top_k_b = st.number_input("Top K B (optional)", 0, 100, st.session_state.params_b["top_k"] or 0, 1,
                                     help="Top-k sampling limits the model to select its next word from only the 'k' most likely next words. This helps prevent the model from choosing highly improbable words, maintaining output quality. 0 disables it.")
            
            st.session_state.params_b = {
                "temperature": temp_b,
                "top_p": top_p_b,
                "max_tokens": max_tokens_b,
                "top_k": top_k_b if top_k_b > 0 else None
            }
    
    # Generate button
    if st.button("🚀 Generate Responses", key="btn_generate", type="primary") and llm_client and prompt:
        with st.spinner("Generating responses..."):
            response_a, response_b = llm_client.generate_dual_responses(
                prompt,
                st.session_state.model_a,
                st.session_state.model_b,
                params_a=st.session_state.params_a,
                params_b=st.session_state.params_b
            )
            st.session_state.responses = [response_a, response_b]
            st.rerun()

    # Display responses and regeneration controls
    if st.session_state.responses:
        st.divider()
        st.header("2. Compare Responses")
        
        # Prompt editing
        with st.expander("✏️ Edit Prompt", expanded=False):
            new_prompt = st.text_area("Modify prompt and regenerate:", value=st.session_state.current_prompt, height=100)
            if st.button("🔄 Regenerate Both with New Prompt"):
                st.session_state.current_prompt = new_prompt
                with st.spinner("Regenerating both responses..."):
                    response_a, response_b = llm_client.regenerate_both_responses(
                        new_prompt,
                        st.session_state.model_a,
                        st.session_state.model_b,
                        params_a=st.session_state.params_a,
                        params_b=st.session_state.params_b
                    )
                    st.session_state.responses = [response_a, response_b]
                st.rerun()
        
        # Display Responses Side-by-Side with regeneration controls
        r_col1, r_col2 = st.columns(2)
        
        with r_col1:
            st.subheader("Response A")
            st.caption(f"Model: {st.session_state.model_a}")
            st.caption(f"Temp: {st.session_state.params_a['temperature']} | Top-P: {st.session_state.params_a['top_p']} | Max Tokens: {st.session_state.params_a['max_tokens']}")
            
            if st.button("🔄 Regenerate Response A", key="regen_a"):
                with st.spinner("Regenerating Response A..."):
                    response_a = llm_client.regenerate_response(
                        st.session_state.current_prompt,
                        st.session_state.model_a,
                        **st.session_state.params_a
                    )
                    st.session_state.responses[0] = response_a
                st.rerun()
            
            st.markdown(st.session_state.responses[0])
        
        with r_col2:
            st.subheader("Response B")
            st.caption(f"Model: {st.session_state.model_b}")
            st.caption(f"Temp: {st.session_state.params_b['temperature']} | Top-P: {st.session_state.params_b['top_p']} | Max Tokens: {st.session_state.params_b['max_tokens']}")
            
            if st.button("🔄 Regenerate Response B", key="regen_b"):
                with st.spinner("Regenerating Response B..."):
                    response_b = llm_client.regenerate_response(
                        st.session_state.current_prompt,
                        st.session_state.model_b,
                        **st.session_state.params_b
                    )
                    st.session_state.responses[1] = response_b
                st.rerun()
            
            st.markdown(st.session_state.responses[1])
        
        # Regenerate both button
        if st.button("🔄 Regenerate Both Responses", type="secondary"):
            with st.spinner("Regenerating both responses..."):
                response_a, response_b = llm_client.regenerate_both_responses(
                    st.session_state.current_prompt,
                    st.session_state.model_a,
                    st.session_state.model_b,
                    params_a=st.session_state.params_a,
                    params_b=st.session_state.params_b
                )
                st.session_state.responses = [response_a, response_b]
            st.rerun()
        
        st.divider()
        st.header("3. Evaluate Responses")
        
        # Rubric Selection
        rubric_files = rubric_builder.list_rubrics()
        
        # Create display names for rubrics
        rubric_options = {rubric_builder.get_rubric_display_name(f): f for f in rubric_files}
        
        selected_display = st.selectbox(
            "Select Evaluation Rubric",
            list(rubric_options.keys()),
            help="Choose the rubric that matches your prompt task type"
        )
        
        if selected_display:
            selected_file = rubric_options[selected_display]
            rubric = rubric_builder.load_rubric(selected_file)
            st.session_state.selected_rubric = rubric
            
            # Display rubric information
            st.subheader(f"📋 {rubric.get('name', 'Evaluation Rubric')}")
            st.info(f"**Scenario**: {rubric.get('scenario', 'Unknown')}")
            if rubric.get('use_case'):
                st.caption(f"**Use for**: {rubric.get('use_case', '')}")

            # --- Evaluation Mode Toggle ---
            eval_mode = st.radio(
                "Evaluation Mode",
                ["Manual Evaluation", "🤖 Auto-Evaluation (LLM-as-Judge)"],
                horizontal=True,
                help="Choose to evaluate manually or let an LLM automatically judge the responses"
            )
            st.session_state.eval_mode = eval_mode
            
            if eval_mode == "Manual Evaluation":
                # ===== MANUAL EVALUATION FLOW (unchanged) =====
                scores_a = {}
                scores_b = {}
                
                rating_options = ["3 - No Issues", "2 - Minor Issues", "1 - Major Issues"]
                
                for dim in rubric.get("dimensions", []):
                    st.markdown(f"**{dim['name']}** (Weight: {dim['weight']})")
                    st.caption(dim['description'])
                    
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        st.subheader("Response A")
                        opt_a = st.radio(f"Rating A - {dim['name']}", rating_options, key=f"rad_a_{dim['name']}", horizontal=True, label_visibility="collapsed")
                        score_a = int(opt_a.split(" - ")[0])
                        
                        comment_a = ""
                        if score_a < 3:
                            comment_a = st.text_area(f"Comment A - {dim['name']}", placeholder="Describe the issues...", key=f"com_a_{dim['name']}", height=80)
                        
                        scores_a[dim['name']] = {'score': score_a, 'comment': comment_a}

                    with c2:
                        st.subheader("Response B")
                        opt_b = st.radio(f"Rating B - {dim['name']}", rating_options, key=f"rad_b_{dim['name']}", horizontal=True, label_visibility="collapsed")
                        score_b = int(opt_b.split(" - ")[0])
                        
                        comment_b = ""
                        if score_b < 3:
                            comment_b = st.text_area(f"Comment B - {dim['name']}", placeholder="Describe the issues...", key=f"com_b_{dim['name']}", height=80)
                            
                        scores_b[dim['name']] = {'score': score_b, 'comment': comment_b}
                        
                    st.divider()
                
                if st.button("Submit Evaluations", type="primary"):
                    res_a = evaluator.format_results(rubric, scores_a)
                    res_b = evaluator.format_results(rubric, scores_b)
                    
                    st.session_state.evaluation_complete = True
                    st.session_state.final_scores = {"a": res_a['final_score'], "b": res_b['final_score']}
                    st.session_state.current_scores_a = scores_a
                    st.session_state.current_scores_b = scores_b
                    st.session_state.auto_eval_data = None  # Clear any auto-eval data
                    
            else:
                # ===== AUTO-EVALUATION FLOW (LLM-as-Judge) =====
                st.markdown("---")
                st.markdown("### 🤖 Automated Evaluation")
                st.caption("An LLM will act as judge and evaluate both responses across all rubric dimensions automatically.")
                
                # Judge model selection
                if llm_client:
                    free_models_judge = llm_client.get_free_models()
                    judge_model_options = [f"{m['name']} ({m['id']})" for m in free_models_judge]
                    judge_model_ids = {f"{m['name']} ({m['id']})": m['id'] for m in free_models_judge}
                    
                    if judge_model_options:
                        selected_judge = st.selectbox(
                            "Select Judge Model:",
                            judge_model_options,
                            key="judge_model_select",
                            help="Choose which LLM will evaluate the responses. More capable models produce better judgements."
                        )
                        judge_model_id = judge_model_ids[selected_judge]
                        
                        if st.button("🤖 Run Auto-Evaluation", key="btn_auto_eval", type="primary"):
                            auto_eval = AutoEvaluator(llm_client)
                            
                            with st.spinner("🤖 LLM Judge is analyzing both responses..."):
                                try:
                                    result = auto_eval.auto_evaluate(
                                        prompt=st.session_state.current_prompt,
                                        response_a=st.session_state.responses[0],
                                        response_b=st.session_state.responses[1],
                                        rubric=rubric,
                                        judge_model=judge_model_id
                                    )
                                    
                                    # Store auto-evaluation results in session state
                                    st.session_state.auto_eval_data = result
                                    st.session_state.current_scores_a = result['scores_a']
                                    st.session_state.current_scores_b = result['scores_b']
                                    st.session_state.preferred_response = result['preferred_response']
                                    st.session_state.user_justification = result['justification']
                                    
                                    res_a = evaluator.format_results(rubric, result['scores_a'])
                                    res_b = evaluator.format_results(rubric, result['scores_b'])
                                    
                                    st.session_state.evaluation_complete = True
                                    st.session_state.final_scores = {"a": res_a['final_score'], "b": res_b['final_score']}
                                    
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Auto-evaluation failed: {str(e)}")
                
                # Display auto-evaluation results if available
                if st.session_state.auto_eval_data and st.session_state.evaluation_complete:
                    st.success("✅ Auto-Evaluation Complete!")
                    
                    # Show dimension-by-dimension results
                    st.markdown("### 📊 Dimension Scores")
                    
                    score_labels = {3: "✅ No Issues", 2: "⚠️ Minor Issues", 1: "❌ Major Issues"}
                    
                    for dim in rubric.get("dimensions", []):
                        dim_name = dim['name']
                        data_a = st.session_state.current_scores_a.get(dim_name, {'score': 0, 'comment': ''})
                        data_b = st.session_state.current_scores_b.get(dim_name, {'score': 0, 'comment': ''})
                        
                        st.markdown(f"**{dim_name}** (Weight: {dim['weight']})")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            score_a = data_a.get('score', 0)
                            st.markdown(f"**Response A:** {score_labels.get(score_a, 'N/A')}")
                            if data_a.get('comment'):
                                st.caption(f"💬 {data_a['comment']}")
                        with col_b:
                            score_b = data_b.get('score', 0)
                            st.markdown(f"**Response B:** {score_labels.get(score_b, 'N/A')}")
                            if data_b.get('comment'):
                                st.caption(f"💬 {data_b['comment']}")
                        st.divider()
                    
                    # Show judge justification
                    st.markdown("### 📝 Judge's Comparative Justification")
                    st.info(f"**Preferred Response:** Response {st.session_state.preferred_response}")
                    st.markdown(st.session_state.user_justification)
            
            # ===== RESULTS & EXPORT (shared by both modes) =====
            if st.session_state.evaluation_complete:
                if st.session_state.eval_mode == "Manual Evaluation":
                    st.success("Evaluations Submitted!")
                 
                res_a = evaluator.format_results(rubric, st.session_state.current_scores_a)
                res_b = evaluator.format_results(rubric, st.session_state.current_scores_b)

                st.markdown("### Final Score Comparison")
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    ui.metric_card(title="Response A Final Score", content=f"{res_a['final_score']:.2f}/10", description="Weighted Score")
                with res_col2:
                    ui.metric_card(title="Response B Final Score", content=f"{res_b['final_score']:.2f}/10", description="Weighted Score")
            
            # Export Evaluation Report Section
            if st.session_state.evaluation_complete:
                st.divider()
                st.header("4. Export Evaluation Report")
                
                st.markdown("Provide your comparative analysis and export a comprehensive report.")
                
                # User Justification Input
                justification_label = "Evaluator's Comparative Justification & Insights:"
                justification_placeholder = "Explain which response is better and why. Include your reasoning based on the dimension scores and any key differentiators you observed."
                
                if st.session_state.auto_eval_data:
                    justification_label = "Judge's Justification (editable):"
                    justification_placeholder = "The LLM judge's justification is pre-filled below. You can edit it if needed."
                
                user_justification = st.text_area(
                    justification_label,
                    value=st.session_state.user_justification,
                    height=150,
                    placeholder=justification_placeholder
                )
                st.session_state.user_justification = user_justification
                
                # Preferred Response Selection
                col_pref, col_model = st.columns(2)
                
                with col_pref:
                    preferred = st.radio(
                        "Preferred Response:",
                        ["A", "B"],
                        index=0 if st.session_state.preferred_response == "A" else 1,
                        horizontal=True
                    )
                    st.session_state.preferred_response = preferred
                
                # Report Model Selection
                with col_model:
                    if llm_client:
                        free_models_export = llm_client.get_free_models()
                        export_model_options = [f"{m['name']} ({m['id']})" for m in free_models_export]
                        export_model_ids = {f"{m['name']} ({m['id']})": m['id'] for m in free_models_export}
                        
                        if export_model_options:
                            default_idx = 0
                            if st.session_state.report_model and st.session_state.report_model in export_model_ids.values():
                                for idx, model_id in enumerate(export_model_ids.values()):
                                    if model_id == st.session_state.report_model:
                                        default_idx = idx
                                        break
                            
                            selected_export_model = st.selectbox(
                                "Report Analysis Model:",
                                export_model_options,
                                index=default_idx,
                                help="Select which model will generate the enhanced response and reasoning analysis"
                            )
                            st.session_state.report_model = export_model_ids[selected_export_model]
                
                # Export Button
                export_enabled = (
                    st.session_state.evaluation_complete
                    and user_justification.strip() != ""
                    and st.session_state.report_model is not None
                )
                
                # Determine evaluator label
                evaluator_label = 'User'
                if st.session_state.auto_eval_data:
                    evaluator_label = f'LLM-as-Judge'
                
                if st.button(
                    "📄 Export Evaluation Report",
                    key="btn_export",
                    type="primary",
                ) and export_enabled:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    session_data = {
                        'prompt': st.session_state.current_prompt,
                        'response_a': st.session_state.responses[0],
                        'response_b': st.session_state.responses[1],
                        'model_a': st.session_state.model_a,
                        'model_b': st.session_state.model_b,
                        'params_a': st.session_state.params_a,
                        'params_b': st.session_state.params_b,
                        'rubric': st.session_state.selected_rubric,
                        'scores_a': st.session_state.current_scores_a,
                        'scores_b': st.session_state.current_scores_b,
                        'final_score_a': st.session_state.final_scores['a'],
                        'final_score_b': st.session_state.final_scores['b'],
                        'user_justification': st.session_state.user_justification,
                        'preferred_response': st.session_state.preferred_response,
                        'timestamp': timestamp,
                        'evaluator': evaluator_label,
                        'report_model': st.session_state.report_model
                    }
                    
                    report_gen = ReportGenerator(llm_client)
                    
                    with st.spinner("🤖 Generating enhanced analysis and reasoning..."):
                        try:
                            report_content = report_gen.generate_report(
                                session_data,
                                st.session_state.report_model
                            )
                            
                            eval_dir = Path('evaluations')
                            eval_dir.mkdir(exist_ok=True)
                            report_filename = f"evaluation_report_{timestamp}.md"
                            report_path = eval_dir / report_filename
                            report_path.write_text(report_content, encoding='utf-8')
                            
                            st.success(f"✅ Report generated successfully: `{report_filename}`")
                            
                            st.download_button(
                                "⬇️ Download Report",
                                report_content,
                                file_name=report_filename,
                                mime="text/markdown",
                                type="secondary"
                            )
                            
                            with st.expander("📄 Preview Report", expanded=False):
                                st.markdown(report_content)
                                
                        except Exception as e:
                            st.error(f"❌ Error generating report: {str(e)}")
                
                if not export_enabled and not user_justification.strip():
                    st.info("💡 Please provide your comparative justification above to enable export.")

def render_prompt_analysis_page(analyzer, llm_client):
    st.header("Prompt Enhancement Analysis")
    
    prompt = st.text_area("Enter a prompt to analyze:", height=200, value=st.session_state.current_prompt)
    
    if llm_client:
        free_models = llm_client.get_free_models()
        model_options = [f"{m['name']} ({m['id']})" for m in free_models]
        model_ids = {f"{m['name']} ({m['id']})": m['id'] for m in free_models}
        
        if not model_options:
            st.warning("No free models available. Please check your API key or try again later.")
            return
            
        selected_model = st.selectbox(
            "Select LLM for Analysis:",
            model_options,
            help="Choose the model that will analyze your prompt and suggest improvements."
        )
        model_id = model_ids[selected_model]
        
        if st.button("Analyze Prompt with LLM"):
            if not prompt.strip():
                st.warning("Please enter a prompt to analyze.")
                return
                
            with st.spinner("Analyzing prompt..."):
                analysis_result = analyzer.analyze_with_llm(prompt, llm_client, model_id)
                
                st.markdown("### 🤖 LLM Analysis & Suggestions")
                st.markdown(analysis_result)
    else:
        st.warning("Please enter your OpenRouter API key in the sidebar to use LLM analysis.")

def render_rubric_builder(builder):
    st.header("Custom Rubric Builder")
    
    with st.form("rubric_form"):
        name = st.text_input("Rubric Name")
        desc = st.text_area("Description")
        
        # Simple implementation: Text area for JSON/YAML editing or complex UI
        # For MVP, let's use a simple text area to edit YAML directly or instructions
        st.warning("Advanced UI builder coming in Phase 2. Ensure YAML format.")
        
        template = builder.get_empty_rubric()
        # Pre-fill with template if empty
        
        yaml_content = st.text_area("Rubric YAML Definition", value=yaml.dump(template, sort_keys=False), height=400)
        
        if st.form_submit_button("Save Rubric"):
            try:
                data = yaml.safe_load(yaml_content)
                filename = f"{name.lower().replace(' ', '_')}.yaml"
                if builder.save_rubric(filename, data):
                    st.success(f"Rubric saved as {filename}")
                else:
                    st.error("Failed to save rubric.")
            except Exception as e:
                st.error(f"Invalid YAML: {e}")

if __name__ == "__main__":
    main()
