import streamlit as st
import pandas as pd
from pathlib import Path
import yaml
import os

from config import (
    APP_TITLE, APP_ICON, RUBRICS_DIR, TECHNIQUES_DIR
)
import config
from utils.llm_client import LLMClient
from utils.rubric_builder import RubricBuilder
from utils.prompt_analyzer import PromptAnalyzer
from utils.evaluator import Evaluator

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

def main():
    st.title(f"{APP_ICON} {APP_TITLE}")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Generate & Evaluate", "Prompt Analysis", "Rubric Builder"])
    
    # API Key Handling
    api_key = st.sidebar.text_input("Anthropic API Key", type="password", value=os.getenv("ANTHROPIC_API_KEY", ""))
    if api_key:
        llm_client = LLMClient(api_key=api_key)
    else:
        st.sidebar.warning("Please enter your API Key to use AI features.")
        llm_client = None

    if page == "Generate & Evaluate":
        render_generate_page(llm_client)
    elif page == "Prompt Analysis":
        render_prompt_analysis_page(prompt_analyzer)
    elif page == "Rubric Builder":
        render_rubric_builder(rubric_builder)

def render_generate_page(llm_client):
    st.header("1. Generate Responses")
    
    prompt = st.text_area("Enter your prompt:", height=150, value=st.session_state.current_prompt)
    st.session_state.current_prompt = prompt
    
    model = st.selectbox("Select Model", ["claude-3-opus-20240229", "claude-3-sonnet-20240229"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Responses", type="primary", disabled=not llm_client):
            with st.spinner("Generating..."):
                responses = llm_client.generate_multiple_responses(prompt, count=2, model=model)
                st.session_state.responses = responses
    
    if st.session_state.responses:
        st.divider()
        st.header("2. Evaluate Responses")
        
        # Display Responses Side-by-Side
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            st.subheader("Response A")
            st.markdown(st.session_state.responses[0])
        with r_col2:
            st.subheader("Response B")
            st.markdown(st.session_state.responses[1])
            
        st.divider()
        
        # Rubric Selection
        rubric_files = rubric_builder.list_rubrics()
        selected_file = st.selectbox("Select Evaluation Rubric", rubric_files)
        
        if selected_file:
            rubric = rubric_builder.load_rubric(selected_file)
            st.session_state.selected_rubric = rubric
            
            st.subheader(f"Evaluation: {rubric.get('name', 'Unknown')}")
            st.markdown(rubric.get('description', ''))
            
            # Evaluation Form
            scores_a = {}
            scores_b = {}
            
            for dim in rubric.get("dimensions", []):
                st.markdown(f"**{dim['name']}** (Weight: {dim['weight']})")
                st.caption(dim['description'])
                
                c1, c2 = st.columns(2)
                with c1:
                    scores_a[dim['name']] = st.slider(f"Score A - {dim['name']}", 0, 10, 5, key=f"a_{dim['name']}")
                with c2:
                    scores_b[dim['name']] = st.slider(f"Score B - {dim['name']}", 0, 10, 5, key=f"b_{dim['name']}")
                st.divider()
            
            # Calculate & Display Results
            if st.button("Calculate Scores"):
                res_a = evaluator.format_results(rubric, scores_a)
                res_b = evaluator.format_results(rubric, scores_b)
                
                st.success("Evaluation Complete!")
                
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.metric("Response A Final Score", f"{res_a['final_score']:.2f}/10")
                with res_col2:
                    st.metric("Response B Final Score", f"{res_b['final_score']:.2f}/10")

def render_prompt_analysis_page(analyzer):
    st.header("Prompt Enhancement Analysis")
    
    prompt = st.text_area("Enter a prompt to analyze:", height=200, value=st.session_state.current_prompt)
    
    if st.button("Analyze Prompt"):
        suggestions = analyzer.analyze(prompt)
        
        if not suggestions:
            st.success("Great prompt! No critical improvements detected based on standard techniques.")
        else:
            st.info(f"Found {len(suggestions)} potential improvements.")
            
            for sug in suggestions:
                with st.expander(f"💡 {sug['name']}"):
                    st.write(f"**Why:** {sug['description']}")
                    st.write("**Checklist:**")
                    for item in sug['checklist']:
                        st.write(f"- {item}")
                    st.markdown(f"**Example:** {sug['example_enhancement']}")

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
