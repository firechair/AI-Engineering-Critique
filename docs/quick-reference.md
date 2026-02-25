# Evaluation Quick Reference

A cheat sheet for evaluating LLM responses.

---

## Choosing a Rubric

```
What's your task type?
├─ Code/Algorithms       → Coding Rubric
├─ Docs/Guides/Tutorials → Technical Writing Rubric
├─ System Design         → System Architecture Rubric
├─ Creative/Marketing    → Creative Writing Rubric
└─ Research/Data         → Research Analysis Rubric
```

### Available Rubrics

| Rubric | File | Focus Areas |
|--------|------|-------------|
| **Coding** | `coding-rubric.md` | Accuracy, correctness, quality, safety |
| **Technical Writing** | `technical-writing-rubric.md` | Accuracy, clarity, structure, usability |
| **System Architecture** | `system-architecture-rubric.md` | Design quality, trade-offs, scalability |
| **Creative Writing** | `creative-writing-rubric.md` | Creativity, engagement, voice |
| **Research Analysis** | `research-analysis-rubric.md` | Accuracy, rigor, objectivity |

---

## The 3-Point Rating Scale

All rubrics use the same scale:

| Score | Meaning | When to Use |
|-------|---------|-------------|
| **3** | No Issues | Meets all criteria, nothing wrong |
| **2** | Minor Issues | Small problems, up to 3 minor mistakes |
| **1** | Major Issues | Significant problems, severely impacts usefulness |

---

## Dimension Overview (Coding Rubric)

### Critical Dimensions (Address First)

**Requirements Compliance** (Weight: ~20%)
- Does it address all prompt requirements?
- Does it follow all constraints?
- Does it satisfy user intent?

**Technical Accuracy** (Weight: ~20%)
- Does the code execute correctly?
- Does it produce correct outputs?
- Are explanations accurate?

### Important Dimensions

**Code Quality** (Weight: ~15%)
- Well-structured?
- Good naming?
- Proper formatting?
- Follows conventions?

**Safety & Robustness** (Weight: ~10%)
- Error handling?
- Security considered?
- Edge cases handled?

### Nice-to-Have Dimensions

**Completeness & Depth** (Weight: ~15%)
- Thorough explanation?
- States assumptions?
- Sufficient detail?

**Conciseness & Focus** (Weight: ~10%)
- No unnecessary repetition?
- Stays on topic?
- No fluff?

**Presentation & Clarity** (Weight: ~10%)
- Well-organized?
- Good formatting?
- Easy to understand?

---

## Overall Quality Assessment

| Rating | What It Means |
|--------|---------------|
| **Perfect** | All dimensions = 3 |
| **Good** | At most 1 dimension = 2 |
| **Acceptable** | 2-3 dimensions = 2, or usable but could improve |
| **Poor** | 1 dimension = 1, OR 4+ dimensions = 2 |
| **Unacceptable** | 2+ dimensions = 1 |

---

## Comparing Two Responses

Use this scale when picking a winner:

| Score | Meaning |
|-------|---------|
| **+2** | Response A is significantly better |
| **+1** | Response A is somewhat better |
| **0** | They're roughly equivalent |
| **-1** | Response B is somewhat better |
| **-2** | Response B is significantly better |

---

## Score Mapping in the App

The app uses 0-10 sliders. Map your 3-point scores like this:

| Your Assessment | Slider Range |
|-----------------|--------------|
| Major Issues (1) | 0–3 |
| Minor Issues (2) | 4–7 |
| No Issues (3) | 8–10 |

---

## Evaluation Workflow

### Single Response
1. Read the prompt carefully
2. Test the code (if applicable)
3. Rate each dimension (1-3)
4. Explain any non-3 ratings
5. Assign overall quality

### Comparing Two Responses
1. Evaluate both independently
2. Identify key differences
3. Determine preference (-2 to +2)
4. Write justification (2-4 sentences)
5. Verify ratings match your preference

---

## Writing Justifications

Use this template:

```
[Conclusion: Which is better and why — 1 sentence]
[Evidence: Cite specific differences — 1-2 sentences]
[Impact: Why it matters for this task — 1 sentence]
```

**Example:**
> Response A is somewhat better (+1). Response A includes comprehensive
> error handling with try-catch blocks for all API calls, while Response B
> only handles the primary error case. For a production system interfacing
> with external APIs, robust error handling is critical.

---

## Common Mistakes to Avoid

**When Rating:**
- Don't penalize style differences unless they hurt readability
- Don't assume errors without testing the code
- Don't mark "Major Issue" if it works for the main use cases
- Don't overlook security issues in web/data code

**When Comparing:**
- Don't discuss dimensions where both responses score 3
- Don't use vague language ("seems better", "looks nicer")
- Don't write long justifications — be concise
- Don't quote large portions of the responses

---

## Quick Decision Tree

```
Does it meet requirements?
├─ No  → Score 1 on Requirements
└─ Yes
   └─ Does the code work?
      ├─ No  → Score 1 on Technical Accuracy
      └─ Yes
         └─ Is it secure and robust?
            ├─ No  → Check severity (1 or 2)
            └─ Yes
               └─ Is it maintainable?
                  ├─ No  → Score 2 on Code Quality
                  └─ Yes → Likely Good or Perfect!
```

---

## Before Submitting Your Evaluation

- [ ] Tested the code (if applicable)
- [ ] Rated all dimensions
- [ ] Explained any non-3 scores
- [ ] Assigned overall quality rating
- [ ] If comparing: determined preference (-2 to +2)
- [ ] If comparing: wrote 2-4 sentence justification
- [ ] Verified no contradictions between ratings and preference
