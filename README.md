# AI Engineering Critique

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> "I don't just use AI—I systematically evaluate, improve, and architect AI solutions."

## 🎯 Project Overview

This repository showcases a systematic approach to AI Engineering, focusing on rigorous evaluation, prompt engineering, and architectural thinking. It demonstrates how to move beyond simple prompting to build reliable, high-quality AI systems through iterative improvement and structured critique.

The project highlights expertise in:
- **AI Output Evaluation**: Systematically assessing AI responses using multi-dimensional rubrics.
- **AI-Generated Code Review**: Applying architectural principles to review and improve AI code.
- **Prompt Design & Analysis**: Analyzing prompts to identify weaknesses and applying techniques for better results.
- **Systematic Thinking**: Using frameworks and checklists to ensure consistent quality.

## 📋 Project Goals

This repository aims to demonstrate:
1. ✅ **Reasoning**: How I reason about AI outputs and identify subtleties.
2. ✅ **Evaluation**: How I evaluate systems systematically using defined criteria.
3. ✅ **Iteration**: How I improve AI outputs through iterative refinement.
4. ✅ **Architecture**: How I think like a reviewer/architect when designing AI solutions.

## 🏗️ Repository Structure

```
ai-engineering-critique/
├── streamlit-app/                     # 🚀 Interactive evaluation tool
│   ├── app.py                         # Main application
│   ├── rubrics/                       # YAML definitions for evaluation criteria
│   ├── prompt_techniques/             # Techniques for prompt enhancement
│   └── utils/                         # Helper logic for LLM, analysis, etc.
│
├── case-studies/                      # 📚 Deep-dive analyses of specific problems
│   └── 001-rate-limiter-design/       # Example: Designing a rate limiter
│
├── prompt-iterations/                 # 🔄 Journeys of prompt refinement
│   └── 001-api-documentation/         # Example: Improving API docs
│
├── framework/                         # 🧠 Methodology and guides
│   ├── evaluation-criteria.md         # Standard dimensions for evaluation
│   ├── prompt-patterns.md             # Effective prompt patterns
│   └── review-checklist.md            # Systematic review process
│
└── docs/                              # 📖 Usage documentation
    └── how-to-use-app.md              # Guide for the Streamlit app
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- An Anthropic API key (for the AI features)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-engineering-critique.git
   cd ai-engineering-critique
   ```

2. Install dependencies:
   ```bash
   pip install -r streamlit-app/requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root or export the key directly:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   ```

### Running the App

Launch the Streamlit application to start evaluating and improving prompts:

```bash
streamlit run streamlit-app/app.py
```

## 🎨 Features

The interactive Streamlit application included in this repository allows you to:

- **Compare Responses**: Generate and evaluate two AI responses side-by-side.
- **Build Rubrics**: Create custom evaluation criteria or use pre-defined templates.
- **Enhance Prompts**: Get automated suggestions to improve your prompts using proven techniques.
- **Track Scores**: Quantify performance across dimensions like Correctness, Clarity, and Best Practices.

## 📚 Documentation

- [**Framework**](./framework/README.md): Detailed explanation of the evaluation methodology.
- [**Case Studies**](./case-studies/README.md): Real-world examples of this methodology in action.
- [**Prompt Iterations**](./prompt-iterations/README.md): Logs of how prompts evolved to solve specific problems.

## 🤝 Contributing

Contributions are welcome! Please check [CONTRIBUTING.md](./docs/contributing.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
