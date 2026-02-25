# Technical Writing & Documentation Evaluation Rubric

## Overview

This document defines the evaluation framework for assessing AI-generated technical writing, documentation, tutorials, and educational content across multiple quality dimensions. Each dimension is rated on a 3-point scale, and responses receive an overall quality assessment based on the combined ratings.

---

## Rating Scale

All dimensions use the following rating scale:

- **3 - No Issues**: Response meets all criteria with no identifiable problems
- **2 - Minor Issues**: Response has small problems that don't significantly impact usefulness (up to 3 minor mistakes are still considered minor issues)
- **1 - Major Issues**: Response has significant problems that severely impact usefulness

---

## Evaluation Dimensions

### 1. Accuracy & Correctness

**Definition**: Factual correctness, absence of hallucinations, and technical precision in all claims and explanations.

#### What to Evaluate:
- Is all technical information factually correct?
- Are there any hallucinations or fabricated details?
- Are claims supported by evidence or sound reasoning?
- Are technical terms used correctly and precisely?
- Is there a clear distinction between facts and opinions?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | All information accurate, no errors, technically sound throughout. | - All code examples work correctly<br>- API documentation matches actual behavior<br>- Technical concepts explained accurately |
| **2 - Minor Issues** | Mostly accurate with minor factual slip-ups or imprecisions that don't fundamentally mislead. | - One minor technical inaccuracy in explanation<br>- Slightly outdated but still functional approach<br>- Minor terminology imprecision |
| **1 - Major Issues** | Contains significant errors, hallucinations, or fundamentally misleading information. | - Fabricated API methods or parameters<br>- Incorrect algorithm explanations<br>- Major factual errors that would break implementation<br>- Hallucinated library features |

#### Best Practices:
- Verify technical claims against authoritative sources
- Test all code examples before rating as "No Issues"
- Check that API references match actual documentation
- Ensure version-specific information is clearly labeled

---

### 2. Completeness & Depth

**Definition**: Whether all necessary information is covered with appropriate detail, including context, background, prerequisites, and examples.

#### What to Evaluate:
- Does the response address all parts of the prompt?
- Is necessary context and background information included?
- Are prerequisites or dependencies mentioned?
- Are helpful examples provided?
- Does it explain "why" not just "how"?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Comprehensive coverage with appropriate depth. All necessary details included, proper context provided. | - Covers all requested topics thoroughly<br>- Includes relevant prerequisites<br>- Provides working examples<br>- Explains rationale behind approaches |
| **2 - Minor Issues** | Covers main points but missing some helpful context, examples, or explanatory depth. | - Missing one prerequisite mention<br>- Could use additional example<br>- Lacks some helpful background context<br>- Doesn't fully explain the "why" |
| **1 - Major Issues** | Incomplete, missing critical information or context that makes the content unusable. | - Skips major sections of the requested topic<br>- No examples when essential<br>- Missing critical prerequisites<br>- Too shallow to be actionable |

#### Balance Point:
- **Too shallow**: Missing critical information, user can't implement
- **Just right**: Complete coverage, actionable, right level of detail
- **Too detailed**: Overwhelming with unnecessary minutiae (rare for technical writing)

---

### 3. Clarity & Readability

**Definition**: How clearly and understandably the content is communicated to the target audience.

#### What to Evaluate:
- Is unnecessary jargon avoided or explained when used?
- Are sentences clear and well-structured?
- Are main points immediately apparent?
- Are complex concepts broken down effectively?
- Is content appropriate for the target audience level?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Crystal clear, easy to understand, concepts well-explained for target audience. | - Technical terms explained on first use<br>- Clear, concise sentences<br>- Complex ideas broken into digestible parts<br>- No ambiguity in instructions |
| **2 - Minor Issues** | Generally clear but some confusing sections, unexplained terminology, or dense explanations. | - Some jargon not explained<br>- One or two confusing sentences<br>- Could break down complex section better<br>- Minor ambiguity in wording |
| **1 - Major Issues** | Confusing, hard to follow, unclear explanations that impede understanding. | - Heavy unexplained jargon throughout<br>- Convoluted sentence structure<br>- Main points buried or unclear<br>- Assumes knowledge not appropriate for audience |

#### Clarity Checklist:
- [ ] Jargon explained or avoided
- [ ] Short, clear sentences
- [ ] Complex concepts decomposed
- [ ] Appropriate audience level
- [ ] No ambiguous instructions

---

### 4. Structure & Organization

**Definition**: Logical organization, flow, and formatting of content for easy navigation and comprehension.

#### What to Evaluate:
- Is there logical progression of ideas?
- Are headings, lists, and sections used effectively?
- Are transitions between topics smooth?
- Is information ordered appropriately (simple → complex)?
- Is content easy to scan and navigate?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Excellently organized with logical flow, effective formatting, easy to navigate. | - Clear hierarchical structure<br>- Smooth transitions between sections<br>- Appropriate use of lists and headings<br>- Easy to find information |
| **2 - Minor Issues** | Adequately organized but could use better structure, some awkward transitions. | - Some sections could be reorganized<br>- Minor formatting inconsistencies<br>- One or two abrupt transitions<br>- Could benefit from additional headings |
| **1 - Major Issues** | Poorly organized, confusing flow, hard to follow or navigate. | - No clear structure<br>- Random organization of topics<br>- No headings or formatting<br>- Information scattered illogically |

#### Formatting Best Practices:
- Use hierarchical headings (H1 → H2 → H3)
- Use code blocks for all code examples
- Use lists for steps or multiple items
- Use tables for structured comparisons
- Maintain consistent formatting throughout

---

### 5. Conciseness & Focus

**Definition**: Efficiency in conveying information without unnecessary verbosity while staying focused on the topic.

#### What to Evaluate:
- Is content appropriately concise for the topic?
- Are there unnecessary repetitions?
- Does it stay focused on the topic?
- Are tangents and irrelevant information avoided?
- Does it respect the reader's time?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Optimally concise, no fluff, every sentence adds value. Focused on topic. | - Direct, purposeful writing<br>- No repetition<br>- Stays on topic throughout<br>- Appropriate length for complexity |
| **2 - Minor Issues** | Some verbosity or minor redundancy but doesn't significantly hurt usability. | - Some repetitive explanations<br>- Minor tangential information<br>- Could be 20-30% more concise<br>- Occasional off-topic remarks |
| **1 - Major Issues** | Excessively wordy, redundant, or significantly off-topic content. | - Major repetition throughout<br>- Long tangents unrelated to topic<br>- Excessive pleasantries<br>- Could be 50%+ more concise |

#### Verbosity Indicators:
- Repeating the same information multiple times
- Excessive meta-commentary ("As I mentioned before...")
- Long introductions before getting to the point
- Irrelevant background information

---

### 6. Usability & Actionability

**Definition**: Whether the reader can immediately use or apply the information provided.

#### What to Evaluate:
- Are actionable steps or instructions provided?
- Are practical examples or code snippets included?
- Are next steps or calls to action clear?
- Can the reader implement this immediately?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Highly actionable, reader can immediately apply information with working examples. | - Step-by-step instructions<br>- Complete, tested code examples<br>- Clear next steps<br>- Ready to implement |
| **2 - Minor Issues** | Somewhat actionable but needs additional context or minor clarification to implement. | - Examples need minor adaptation<br>- Some steps could be more explicit<br>- Missing one or two setup details<br>- Mostly actionable with effort |
| **1 - Major Issues** | Not actionable, too abstract, or missing key implementation steps. | - Only theoretical discussion<br>- No examples provided<br>- Critical steps omitted<br>- Cannot be implemented from docs |

---

### 7. Style & Professionalism

**Definition**: Appropriate tone, engagement, professional polish, and grammatical correctness.

#### What to Evaluate:
- Is the tone appropriate for technical documentation?
- Is writing professional and polished?
- Is it engaging without being overly casual?
- Is it grammatically correct?
- Is voice consistent throughout?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Perfect tone for technical docs, professional, engaging, grammatically correct. | - Professional but accessible tone<br>- No grammatical errors<br>- Consistent voice<br>- Appropriate formality level |
| **2 - Minor Issues** | Generally appropriate tone with minor grammar issues or slight tone inconsistencies. | - One or two grammatical errors<br>- Slightly inconsistent formality<br>- Minor tone shift in one section<br>- Mostly professional |
| **1 - Major Issues** | Inappropriate tone, unprofessional, or significant grammar problems. | - Overly casual or chatty<br>- Multiple grammatical errors<br>- Inconsistent voice throughout<br>- Inappropriate for technical audience |

#### Tone Guidelines:
- Professional but accessible
- Direct and purposeful
- Avoids excessive pleasantries
- Maintains consistent formality
- Respects reader's expertise

---

## Overall Quality Assessment

After rating individual dimensions, assign an overall quality score:

| Overall Rating | Criteria |
|----------------|----------|
| **Excellent** | All dimensions rated "No Issues". Documentation is publication-ready. |
| **Discrete** | At most 1 dimension has "Minor Issues". Excellent documentation with negligible problems. |
| **Sufficient** | 2-3 dimensions have "Minor Issues". Usable documentation but could be improved. |
| **Inadequate** | 1 dimension has "Major Issues" OR 4+ dimensions have "Minor Issues". Significant problems. |
| **Unacceptable** | 2+ dimensions have "Major Issues". Documentation is fundamentally flawed. |

---

## Response Comparison Methodology

When comparing two documentation responses:

### Step 1: Individual Assessment
Rate each response independently across all dimensions.

### Step 2: Prioritize Dimensions
Not all dimensions carry equal weight for documentation:

- **Critical**: Accuracy & Correctness, Completeness & Depth
- **Important**: Clarity & Readability, Structure & Organization  
- **Nice-to-have**: Conciseness & Focus, Usability & Actionability, Style & Professionalism

A response with perfect style but major inaccuracies is worse than accurate but slightly verbose documentation.

### Step 3: Preference Ranking

| Score | Meaning |
|-------|---------|
| **+2** | Response A significantly better (multiple major advantages) |
| **+1** | Response A somewhat better (clear but modest advantages) |
| **0** | Roughly equivalent (no meaningful difference) |
| **-1** | Response B somewhat better |
| **-2** | Response B significantly better |

### Step 4: Write Justification
Focus only on key differentiators. Keep to 2-4 sentences.

---

## Common Pitfalls to Avoid

### When Rating:
- Don't penalize appropriate depth as "too detailed"
- Don't confuse personal style preferences with actual quality issues
- Don't expect perfect brevity if topic complexity requires detail
- Test code examples before rating accuracy

### When Writing Documentation:
- Don't assume prerequisite knowledge without stating it
- Don't skip the "why" - explain rationale
- Don't use jargon without explanation
- Don't forget practical examples

---

## Use Case Examples

**Perfect for evaluating**:
- API documentation
- Tutorial articles
- How-to guides
- README files
- Technical blog posts
- Installation guides
- Configuration documentation

**Not ideal for**:
- Creative writing or narratives
- Code implementation (use Coding Rubric)
- System design discussions (use Architecture Rubric)
- Research papers (use Research Rubric)

---

## Version History

- **v1.0** - Initial comprehensive technical writing rubric following coding rubric v1.1 format

---

*This rubric guide is designed for the AI Engineering Critique repository to demonstrate systematic evaluation methodology for AI-generated technical documentation.*
