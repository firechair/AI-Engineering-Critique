# AI Engineering Critique

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Ever wondered why the same LLM gives wildly different outputs to the same prompt?**

Or why one model's "helpful" response misses the point while another nails it? The difference isn't magic it's evaluation skill. And that skill is trainable.

This platform helps you develop that skill through hands on practice with **Preference Learning**, the same technique behind RLHF that powers ChatGPT, Claude, and other modern LLMs.

---

## Why Preference Learning Matters

Every major LLM you use today was shaped by human preferences. Engineers didn't just run training code—they learned to see the difference between "good enough" and "actually good." They compared outputs, articulated why one was better, and fed that signal back into the model.

That evaluation skill is valuable beyond model training:

- **Better prompts**: When you understand what makes a response good, you write prompts that get good responses
- **Smarter model selection**: You can objectively compare models for your specific use case
- **Stronger AI integration**: You spot issues before they reach production
- **Cross-language insights**: You discover which models perform better in specific languages

The engineers who can evaluate systematically become force multipliers. This platform is where you build that capability.

---

## What You Can Do Here

**Compare LLM Responses Side by Side**
Generate two responses to the same prompt—either from the same model with different parameters, or from completely different models. See exactly where they diverge.

**Score Against Real Rubrics**
Apply one of 5 pre built rubrics designed for specific scenarios: Coding, Technical Writing, System Architecture, Creative Writing, or Research Analysis. Each rubric breaks evaluation into weighted dimensions.

**Choose Your Evaluation Mode**
Score responses yourself (Manual Evaluation) or let another LLM do it (LLM as Judge). Then compare the results. Where do you agree? Where do you differ? That gap is where learning happens.

**Generate Detailed Reports**
Export your evaluation as a markdown report. The platform adds LLM powered reasoning analysis that identifies points you might have missed and validates your assessment.

**Sharpen Your Prompts**
Before you generate responses, run your prompt through the analyzer. It checks against 6 proven techniques and suggests improvements.

**Build Custom Rubrics**
The prebuilt rubrics don't fit your use case? Create your own with custom dimensions and weights.

---

## Your Learning Path

Here's the typical journey through the platform:

1. **Start with a prompt** — Write something you're genuinely curious about, or paste one that's been giving you trouble

2. **Generate competing responses** — Pick two models, or the same model with different temperature settings

3. **Apply a rubric** — Choose one that matches your task type (coding, writing, analysis, etc.)

4. **Score each dimension** — Use the 3-point scale: No Issues (3), Minor Issues (2), Major Issues (1)

5. **Write your justification** — This is the critical part. Articulate *why* you prefer one response. Be specific.

6. **Generate your report** — Get a full breakdown with LLM reasoning that challenges or validates your assessment

7. **Try LLMasJudge** — Run the same evaluation automatically and compare results

8. **Learn from the gaps** — The differences between your evaluation and the automated one reveal your blind spots

The more evaluations you do, the sharper your eye becomes.

---

## Pre-Built Evaluation Rubrics

| Rubric | Best For | Key Dimensions |
|--------|----------|----------------|
| **Coding** | Code generation, algorithms, implementations | Requirements Compliance, Technical Accuracy, Code Quality, Safety |
| **Technical Writing** | Documentation, tutorials, explanations | Accuracy, Completeness, Clarity, Usability |
| **System Architecture** | Design discussions, scalability questions | Problem Understanding, Tradeoff Analysis, NFRs |
| **Creative Writing** | Stories, marketing copy, blog posts | Creativity, Engagement, Tone, Structure |
| **Research Analysis** | Summaries, literature reviews, data analysis | Evidence, Rigor, Objectivity, Clarity |

**Scoring System**: Each dimension uses a 3 point scale with configurable weights. Final scores normalize to a 10 point scale for easy comparison.

---

## Level Up Your Prompts

Before generating responses, you can analyze and improve your prompts using 6 techniques:

| Technique | What It Does |
|-----------|--------------|
| **Add Context** | Include persona, goal, and target audience |
| **Specify Format** | Define structure, constraints, output type |
| **Few-Shot Examples** | Show input-output pairs for complex tasks |
| **Clarify Constraints** | Set boundaries and restrictions |
| **Chain of Thought** | Request step-by-step reasoning |
| **Evaluation Criteria** | Tell the model how success will be measured |

The Prompt Analysis page provides checklists and examples for each technique.

---

## Quick Start

### Prerequisites
- Python 3.10 or higher
- OpenRouter API key (free tier available at [openrouter.ai](https://openrouter.ai))

### Installation

```bash
git clone <repository-url>
cd ai-engineering-critique
pip install -r streamlit-app/requirements.txt
```

### Configuration

```bash
# Set your API key
export OPENROUTER_API_KEY="your-key-here"

# Or enter it directly in the app sidebar
```

### Run the App

```bash
streamlit run streamlit-app/app.py
```

The app automatically filters to show only free models, so you can experiment without cost.

---

## See It In Action

The repository includes two complete evaluation reports you can study:

- **[Human-Evaluated Report](streamlit-app/evaluations/)** — Manual scoring **made by me** with detailed justification as an example on how to cross-evaluate LLM responses
- **[LLM-as-Judge Report](streamlit-app/evaluations/)** — Automated evaluation for comparison

Both demonstrate real evaluations on coding prompts, including multi language examples (Italian). Study how justifications are structured and how dimension scores translate to final assessments.

---

## Project Structure

```
ai-engineering-critique/
├── streamlit-app/
│   ├── app.py                      # Main application
│   ├── rubrics/                    # 5 pre built evaluation rubrics
│   ├── prompt_techniques/          # 6 techniques for prompt enhancement
│   ├── evaluations/                # Example reports
│   └── utils/                      # LLM client, evaluator, report generator
├── docs/
│   ├── api-setup.md               # OpenRouter configuration
│   ├── how-to-use-app.md          # Detailed usage guide
│   └── quick-reference.md         # Rubric selection, scoring cheat sheet
└── README.md
```

---

## Under the Hood

- **Free Models**: Uses OpenRouter's freetier LLMs—no cost to experiment
- **Parameter Control**: Adjust Temperature, Top-P, Max Tokens, and Top-K for each response
- **Dual Evaluation**: Switch between manual scoring and LLM as Judge
- **Weighted Scoring**: Each rubric dimension has configurable importance
- **Report Generation**: Exports markdown with LLM reasoning analysis

---

## Contributing

Found a bug? Have an idea for a new rubric? Contributions are welcome. Check the [docs/contributing.md](docs/contributing.md) for guidelines.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
