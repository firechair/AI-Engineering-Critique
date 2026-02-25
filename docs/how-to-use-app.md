# How to Use the App

This guide walks you through the main features of the AI Engineering Critique platform.

## Getting Started

1. Launch the app:
   ```bash
   streamlit run streamlit-app/app.py
   ```

2. Enter your OpenRouter API key in the sidebar (see [api-setup.md](./api-setup.md) for details) — the app only uses free models

3. Use the sidebar to switch between the three main sections:
   - **Generate & Evaluate** — Compare and score LLM responses
   - **Prompt Analysis** — Improve your prompts before generating
   - **Rubric Builder** — Create custom evaluation rubrics

---

## Generate & Evaluate

This is the core workflow. You'll generate two responses, compare them, score them against a rubric, and export a report.

### Step 1: Write Your Prompt

Enter the prompt you want to test in the text area. This could be a coding task, a writing request, or any question you want to compare across models.

**Example prompts:**
- "Write a Python function that validates email addresses"
- "Explain how DNS works to a non technical person"
- "Design a rate limiter for an API"

### Step 2: Choose Your Models

You have two comparison modes:

**Same Model, Different Parameters**
- Pick one model
- Adjust parameters (temperature, top-p) to see how they affect output
- Good for understanding parameter sensitivity

**Different Models**
- Pick two different models
- Keep parameters the same
- Good for comparing model capabilities

### Step 3: Adjust Parameters (Optional)

- **Temperature** (0.0–2.0): Higher = more creative/random, Lower = more focused/deterministic
- **Top-P** (0.0–1.0): Controls diversity of word choices
- **Max Tokens**: Limits response length
- **Top-K**: Restricts vocabulary to top K options

For most evaluations, start with temperature 0.7 and top-p 0.9.

### Step 4: Generate Responses

Click **Generate Responses**. The app calls OpenRouter and displays both responses side by side.

You can:
- **Regenerate one response** — Keep Response A, get a new Response B (or vice versa)
- **Edit the prompt** — Modify and regenerate both
- **Regenerate both** — Get fresh responses with current settings

### Step 5: Select a Rubric

Choose the rubric that matches your task type:

| Task | Rubric |
|------|--------|
| Code, algorithms, scripts | Coding |
| Docs, tutorials, explanations | Technical Writing |
| System design, architecture | System Architecture |
| Stories, marketing, blogs | Creative Writing |
| Research, data analysis | Research Analysis |

The app shows the rubric's dimensions and what each one evaluates.

### Step 6: Score the Responses

You have two options:

**Manual Evaluation**
1. For each dimension, rate both responses:
   - **3 — No Issues**: Meets all criteria
   - **2 — Minor Issues**: Small problems (up to 3 minor mistakes)
   - **1 — Major Issues**: Significant problems
2. Add comments explaining any issues you found
3. The app calculates weighted scores (out of 10)

**LLM as Judge (Auto-Evaluation)**
1. Select a judge model from the dropdown
2. Click **Run Auto-Evaluation**
3. The LLM scores both responses and explains its reasoning
4. Review the scores — you can edit the justification if you disagree

### Step 7: Export Your Report

1. Write a comparative justification, explain why you prefer one response
2. Select which response you prefer (A or B)
3. Choose an analysis model for the report
4. Click **Export Evaluation Report**

The report includes:
- Your original prompt
- Both full responses
- Dimension by dimension scores
- Your justification
- LLM powered reasoning analysis (validates or challenges your assessment)

Reports are saved to `streamlit-app/evaluations/` as markdown files.

---

## Prompt Analysis

Use this before generating responses to improve your prompt.

### How It Works

1. Go to the **Prompt Analysis** tab
2. Paste your draft prompt
3. Select an LLM to analyze it
4. Click **Analyze**

The app checks your prompt against 6 techniques:

| Technique | What It Checks |
|-----------|----------------|
| Add Context | Does the prompt include persona, goal, audience? |
| Specify Format | Is the expected output structure clear? |
| Few-Shot Examples | Are there input-output examples? |
| Clarify Constraints | Are boundaries and restrictions stated? |
| Chain of Thought | Does it ask for step-by-step reasoning? |
| Evaluation Criteria | Does it explain how success is measured? |

You'll get:
- A checklist showing which techniques are missing
- Specific suggestions for improvement
- An enhanced version of your prompt

---

## Rubric Builder

Create custom rubrics when the prebuilt ones don't fit your use case.

### How It Works

1. Go to the **Rubric Builder** tab
2. Define your rubric:
   - **Name**: What to call it
   - **Scenario**: What type of task it's for
   - **Dimensions**: The criteria you'll evaluate (e.g., "Accuracy", "Creativity")
3. For each dimension, set:
   - **Description**: What it measures
   - **Weight**: How important it is (weights should sum to 1.0)
   - **Rating Guide**: What 3, 2, and 1 mean for this dimension
4. Click **Save Rubric**

Your custom rubric appears immediately in the evaluation dropdown.

---

## Tips

**Start simple**: Your first few evaluations will feel slow. That's normal. You're building evaluation intuition.

**Be specific in justifications**: "Response A is better" isn't helpful. "Response A handles edge cases that B ignores (empty input, negative numbers)" teaches you something.

**Compare your scores to LLM as Judge**: The gaps reveal your blind spots. Maybe you're too lenient on code quality, or too strict on formatting.

**Use Prompt Analysis first**: A better prompt means better responses to evaluate. It's worth the extra minute.

---

## Troubleshooting

**Models not loading?**
- Check your OpenRouter API key is entered correctly
- Free models have rate limits — wait a minute and try again

**Responses taking too long?**
- Some models are slower than others
- Try a different model or reduce max tokens

**Report not generating?**
- Make sure you've filled in the justification field
- Select a preferred response (A or B)

**Rubric not appearing?**
- Check that dimension weights sum to 1.0
- Save the rubric before trying to use it
