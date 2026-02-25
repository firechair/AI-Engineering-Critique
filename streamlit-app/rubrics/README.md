# Evaluation Rubrics Guide

## Overview

This directory defines a comprehensive suite of evaluation rubrics designed to assess AI-generated responses across various domains. Each rubric is structured as an in-depth markdown specification encompassing evaluation dimensions, standardized rating guidelines, practical examples, and industry best practices.

---

## 📚 Available Rubrics

### 1. [Coding Rubric](./coding-rubric.md)

**Scenario**: Coding and Technical Implementation  
**Use For**: Code generation, algorithms, debugging, technical implementations

**Dimensions** (6 total):
1. Requirements Compliance
2. Technical Accuracy
3. Code Quality  
4. Completeness & Focus
5. Presentation & Clarity
6. Safety

**When to Use**: Evaluating any programming task, code generation, algorithm implementation, or debugging scenarios.

---

### 2. [Technical Writing Rubric](./technical-writing-rubric.md)

**Scenario**: Technical Writing & Documentation  
**Use For**: API docs, tutorials, how-to guides, technical explanations, README files

**Dimensions** (7 total):
1. Accuracy & Correctness
2. Completeness & Depth
3. Clarity & Readability
4. Structure & Organization
5. Conciseness & Focus
6. Usability & Actionability
7. Style & Professionalism

**When to Use**: Documentation, guides, tutorials, technical blog posts, API documentation.

---

### 3. [System Architecture Rubric](./system-architecture-rubric.md)

**Scenario**: System Analysis & Architecture  
**Use For**: System design, architecture proposals, design decisions, scalability analysis

**Dimensions** (7 total):
1. Problem Understanding
2. Solution Approach & Design
3. Trade-off Analysis
4. Scalability & Non-Functional Requirements
5. Practicality & Implementability
6. Clarity & Communication
7. Completeness & Depth

**When to Use**: System design discussions, architecture proposals, technical design documents, migration strategies.

---

### 4. [Creative Writing Rubric](./creative-writing-rubric.md)

**Scenario**: Creative Writing & Content  
**Use For**: Blog posts, stories, marketing copy, social media, narrative content

**Dimensions** (6 total):
1. Creativity & Originality
2. Engagement & Impact
3. Tone & Voice
4. Structure & Flow
5. Language & Style
6. Purpose Achievement

**When to Use**: Creative stories, marketing materials, blog posts, social media content, persuasive writing.

---

### 5. [Research Analysis Rubric](./research-analysis-rubric.md)

**Scenario**: Research & Data Analysis  
**Use For**: Research summaries, data analysis, factual reports, literature reviews

**Dimensions** (7 total):
1. Factual Accuracy & Evidence
2. Analytical Rigor
3. Completeness & Thoroughness
4. Objectivity & Bias
5. Data Presentation & Visualization
6. Structure & Organization
7. Clarity & Accessibility

**When to Use**: Research reports, data analysis, market research, literature reviews, statistical analysis.

---

## 📊 Universal Rating Scale

All rubrics use a consistent **3-point rating scale**:

| Score | Name | Criteria |
|-------|------|----------|
| **3** | No Issues | Meets all criteria with no identifiable problems |
| **2** | Minor Issues | Small problems that don't significantly impact usefulness (up to 3 minor mistakes) |
| **1** | Major Issues | Significant problems that severely impact usefulness |

---

## 🎯 Choosing the Right Rubric

### Decision Tree

```
Determine the target domain for the generated output:
│
├─ Writing CODE or implementing ALGORITHMS?
│  → Use: Coding Rubric
│  
├─ Creating DOCUMENTATION, GUIDES, or TUTORIALS?
│  → Use: Technical Writing Rubric
│
├─ Designing SYSTEMS or discussing ARCHITECTURE?
│  → Use: System Architecture Rubric
│
├─ Creating CREATIVE CONTENT, MARKETING, or STORIES?
│  → Use: Creative Writing Rubric
│
└─ Conducting RESEARCH, ANALYSIS, or REPORTING DATA?
   → Use: Research Analysis Rubric
```

### Quick Reference Matrix

| Task Type | Best Rubric | Critical Dimensions |
|-----------|-------------|---------------------|
| Code, algorithms, scripts | **Coding** | Requirements, Technical Accuracy |
| Docs, tutorials, guides | **Technical Writing** | Accuracy, Completeness, Clarity |
| System design, architecture | **System Architecture** | Problem Understanding, Solution Design, Trade-offs |
| Stories, marketing, blogs | **Creative Writing** | Creativity, Engagement |
| Research, data reports | **Research Analysis** | Factual Accuracy, Analytical Rigor |

---

## 🚀 Using Rubrics in the Streamlit App

### Quick Start

1. **Launch the app**:
   ```bash
   cd ai-engineering-critique
   pip install -r streamlit-app/requirements.txt
   streamlit run streamlit-app/app.py
   ```

2. **Workflow**:
   - Generate responses from two AI models
   - Select the appropriate rubric for your prompt type
   - Score each dimension (0-10 scale, where 0-3 = Major Issues, 4-7 = Minor Issues, 8-10 = No Issues)
   - Calculate final scores
   - Export comprehensive evaluation report

3. **Score Mapping** (temporary until native 3-point UI):
   - **Major Issues (1)** → Slider: 0-3
   - **Minor Issues (2)** → Slider: 4-7
   - **No Issues (3)** → Slider: 8-10

---

## 📖 Rubric Structure

Each comprehensive rubric guide includes:

### Overview
- Purpose and scope
- Universal 3-point rating scale

### Evaluation Dimensions
For each dimension:
- **Definition**: What this dimension evaluates
- **What to Evaluate**: Specific criteria and checkpoints
- **Rating Guidelines**: Detailed table with examples for each score level (3, 2, 1)
- **Best Practices**: Tips for evaluation
- **Common Issues**: What to watch for

### Methodology
- Overall quality assessment framework
- Response comparison methodology
- Dimension prioritization (Critical, Important, Nice-to-have)
- Common pitfalls to avoid

### Examples & Checklists
- Use case examples
- Evaluation checklists
- Example evaluation templates

---

## 💡 Key Features

### Detailed Guidance
Each dimension includes:
- ✅ Clear definitions
- ✅ Specific evaluation criteria
- ✅ Examples for each rating level
- ✅ Common issues and pitfalls

### Consistent Methodology
- Same 3 point rating scale across all rubrics
- Standardized comparison methodology
- Clear dimension prioritization
- Evidence-based evaluation approach

### Scenario-Specific
- Custom dimensions for each task type
- Relevant examples and use cases
- Task appropriate evaluation criteria
- Context-aware best practices

---

## 📝 Using for Case Studies

### Documentation Workflow

1. **Select appropriate rubric** for your prompt type
2. **Generate and evaluate responses** in Streamlit
3. **Export evaluation report** with comprehensive analysis
4. **Reference report** in your case study documentation
5. **Document learnings** and insights

### Example Case Study Structure

```markdown
## Evaluation

**Rubric Used**: [Coding Rubric](rubrics/coding-rubric.md)  
**Task Type**: Python rate limiter implementation  
**Prompt**: "Implement a token bucket rate limiter in Python"

### Response A: GPT-4
| Dimension | Score | Notes |
|-----------|-------|-------|
| Requirements Compliance | 3 | Fully addressed |
| Technical Accuracy | 3 | Correct implementation |
| Code Quality | 2 | Minor naming inconsistencies |
...

**Final Score**: 8.7/10

### Comparative Analysis
Response A provides cleaner code with better documentation,
while Response B has more comprehensive edge case handling...
```

---

## 🔄 Version History

- **v1.0.0** - Initial Release
  - Introduced comprehensive markdown-based evaluation rubrics.
  - Included scenario-specific examples and standardized comparison methodologies.
  - Integrated with the Streamlit evaluation app.

---

## 📚 Related Documentation

- **Evaluation Reports**: `../evaluations/` — Example reports you can study
- **App Usage Guide**: `../../docs/how-to-use-app.md`
- **Quick Reference**: `../../docs/quick-reference.md`

---

## ✨ Benefits

### For AI Evaluation
- **Systematic**: Consistent evaluation methodology
- **Comprehensive**: Detailed criteria for each dimension
- **Evidence-based**: Clear examples and guidelines
- **Transparent**: Explicit rating criteria

### For Portfolio/Showcase
- **Professional**: Demonstrates rigorous evaluation process
- **Documented**: Complete evaluation traces
- **Insightful**: LLM-powered analysis in reports
- **Reproducible**: Clear methodology others can follow

---

*These evaluation models establish a robust, systematic methodology for assessing AI-generated responses across diverse domains, ensuring consistent quality and alignment with architectural standards.*
