# System Architecture & Design Evaluation Rubric

## Overview

This document defines the evaluation framework for assessing AI-generated system architecture proposals, design discussions, and technical problem-solving across multiple quality dimensions. Each dimension is rated on a 3-point scale, and responses receive an overall quality assessment based on the combined ratings.

---

## Rating Scale

All dimensions use the following rating scale:

- **3 - No Issues**: Response meets all criteria with no identifiable problems
- **2 - Minor Issues**: Response has small problems that don't significantly impact usefulness (up to 3 minor mistakes are still considered minor issues)
- **1 - Major Issues**: Response has significant problems that severely impact usefulness

---

## Evaluation Dimensions

### 1. Problem Understanding

**Definition**: Demonstrates clear understanding of the problem, requirements, constraints, and stakeholder needs.

#### What to Evaluate:
- Does the response accurately identify the core problem?
- Are stated and implied requirements recognized?
- Are constraints and limitations understood?
- Are key stakeholders and their needs identified?
- Are clarifying questions asked when appropriate?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Perfect understanding of problem, requirements, and constraints. Demonstrates deep comprehension. | - Correctly identifies all requirements<br>- Recognizes implicit constraints<br>- Understands stakeholder needs<br>- Asks relevant clarifying questions |
| **2 - Minor Issues** | Good understanding with minor misinterpretations or missed nuances. | - Misses one implicit requirement<br>- Slight misunderstanding of one constraint<br>- Most stakeholder needs identified<br>- Generally accurate problem framing |
| **1 - Major Issues** | Fundamentally misunderstands the problem or misses critical requirements. | - Misidentifies core problem<br>- Ignores major constraints<br>- Misses critical requirements<br>- Wrong problem being solved |

#### Common Issues:
- Jumping to solutions without understanding problem
- Missing non-functional requirements
- Ignoring business constraints
- Not asking clarifying questions when needed

---

### 2. Solution Approach & Design

**Definition**: Quality, soundness, and appropriateness of the proposed technical solution or architecture.

#### What to Evaluate:
- Does the solution address the core problem?
- Is it technically sound and feasible?
- Is it appropriate for the scale and context?
- Are components and interactions well-defined?
- Are clear architectural patterns used?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Excellent solution that is technically sound, well-designed, and addresses all requirements. | - Solves the problem effectively<br>- Uses appropriate patterns<br>- Components clearly defined<br>- Scalable and maintainable<br>- Technically feasible |
| **2 - Minor Issues** | Good solution with minor design weaknesses or suboptimal choices. | - Solution works but not optimal<br>- One component poorly defined<br>- Pattern choice questionable<br>- Minor technical concerns |
| **1 - Major Issues** | Flawed approach that is technically unsound, inappropriate, or doesn't solve the problem. | - Won't solve the problem<br>- Technically infeasible<br>- Fundamentally broken design<br>- Inappropriate for scale<br>- Critical components missing |

#### Design Quality Checklist:
- [ ] Addresses core problem
- [ ] Technically feasible
- [ ] Appropriate architectural patterns
- [ ] Clear component boundaries
- [ ] Scalable and maintainable

---

### 3. Trade-off Analysis

**Definition**: Recognition and evaluation of design trade-offs, alternatives, and justified decision-making.

#### What to Evaluate:
- Are key trade-offs identified (CAP theorem, performance vs complexity, etc.)?
- Are alternative approaches discussed?
- Are design decisions justified?
- Are limitations of the chosen approach acknowledged?
- Are multiple quality attributes considered (scalability, maintainability, etc.)?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Comprehensive trade-off analysis with alternatives discussed and decisions well-justified. | - All major trade-offs identified<br>- Alternatives compared<br>- Decisions clearly justified<br>- Limitations acknowledged<br>- Multiple quality attributes considered |
| **2 - Minor Issues** | Some trade-offs discussed but incomplete analysis or insufficient justification. | - Missing one trade-off discussion<br>- Limited alternative analysis<br>- Some decisions not fully justified<br>- Could expand on implications |
| **1 - Major Issues** | No trade-off analysis or ignores obvious alternatives and their implications. | - No trade-offs mentioned<br>- Presents as "only option"<br>- No alternatives considered<br>- Decisions not justified<br>- Ignores major limitations |

#### Common Trade-offs to Consider:
- Consistency vs Availability vs Partition Tolerance (CAP)
- Performance vs Complexity
- Cost vs Performance  
- Time to Market vs Quality
- Flexibility vs Simplicity
- Centralized vs Distributed

---

### 4. Scalability & Non-Functional Requirements

**Definition**: Consideration of scalability, performance, reliability, security, and other non-functional aspects.

#### What to Evaluate:
- Are scalability concerns addressed?
- Are performance implications considered?
- Is reliability and availability discussed?
- Are security considerations mentioned (if relevant)?
- Is monitoring and observability discussed?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Thorough consideration of NFRs with scalability, performance, reliability well-addressed. | - Scalability strategy clear<br>- Performance requirements met<br>- Reliability/availability discussed<br>- Security addressed<br>- Monitoring planned |
| **2 - Minor Issues** | Some NFRs discussed but incomplete coverage or missing details. | - Scalability mentioned but not detailed<br>- Performance briefly touched on<br>- Some NFRs overlooked<br>- Security mentioned minimally |
| **1 - Major Issues** | NFRs ignored or inadequately addressed despite being critical to success. | - No scalability consideration<br>- Performance ignored<br>- Reliability not mentioned<br>- Critical NFRs missing<br>- Won't meet actual requirements |

#### NFR Checklist:
- [ ] Scalability (horizontal/vertical)
- [ ] Performance (latency, throughput)
- [ ] Reliability (uptime, fault tolerance)
- [ ] Security (authentication, authorization, data protection)
- [ ] Observability (monitoring, logging, tracing)
- [ ] Maintainability

---

### 5. Practicality & Implementability

**Definition**: Whether the solution is realistic, actionable, and implementable with available technology and resources.

#### What to Evaluate:
- Can the solution be implemented with available technology?
- Is development complexity and effort considered?
- Is clear implementation guidance provided?
- Are dependencies and prerequisites identified?
- Is the timeline realistic?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Highly practical with clear, realistic path to implementation. | - Uses proven technologies<br>- Realistic complexity assessment<br>- Clear implementation steps<br>- Dependencies identified<br>- Achievable timeline |
| **2 - Minor Issues** | Mostly practical with some unrealistic elements or unclear implementation path. | - Some unproven technology choices<br>- Complexity slightly underestimated<br>- Implementation path needs detail<br>- Minor dependencies missed |
| **1 - Major Issues** | Impractical, infeasible, or no viable implementation path. | - Requires unavailable technology<br>- Grossly underestimates complexity<br>- No implementation guidance<br>- Critical dependencies ignored<br>- Unrealistic timeline |

---

### 6. Clarity & Communication

**Definition**: How clearly the design is explained and communicated to stakeholders.

#### What to Evaluate:
- Are design decisions clearly explained?
- Is effective use of diagrams made (if applicable)?
- Are technical concepts explained well?
- Is there logical flow of information?
- Is the level of detail appropriate?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Crystal clear communication with well-explained design and logical flow. | - Clear, concise explanations<br>- Effective diagrams<br>- Logical information flow<br>- Appropriate detail level<br>- No ambiguity |
| **2 - Minor Issues** | Generally clear with some confusing parts or areas needing better explanation. | - Some sections unclear<br>- Could use diagram<br>- Minor logical gaps<br>- Slightly too detailed or too shallow |
| **1 - Major Issues** | Confusing, poorly explained, or incomprehensible to target audience. | - Unclear explanations<br>- No visual aids when needed<br>- Illogical flow<br>- Wrong detail level<br>- Extremely confusing |

#### Communication Best Practices:
- Use architecture diagrams (C4 model, UML, etc.)
- Explain decisions and rationale
- Structure: Problem → Solution → Trade-offs → Implementation
- Use consistent terminology
- Target appropriate audience level

---

### 7. Completeness & Depth

**Definition**: Coverage of all necessary aspects of the design with appropriate depth.

#### What to Evaluate:
- Are all major components addressed?
- Are data flow and interactions explained?
- Are edge cases and failure modes considered?
- Are deployment and operations discussed (if relevant)?
- Is there sufficient detail for decision-making?

#### Rating Guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| **3 - No Issues** | Comprehensive coverage with all aspects addressed appropriately for the context. | - All components covered<br>- Data flows clear<br>- Failure modes discussed<br>- Operations considered<br>- Sufficient detail |
| **2 - Minor Issues** | Adequate coverage with some gaps or areas needing more depth. | - One component briefly mentioned<br>- Some interactions unclear<br>- Missing some failure scenarios<br>- Operations mentioned minimally |
| **1 - Major Issues** | Incomplete design missing critical aspects required for evaluation. | - Major components not mentioned<br>- Data flow not explained<br>- No failure consideration<br>- Critical gaps throughout<br>- Insufficient detail |

---

## Overall Quality Assessment

After rating individual dimensions, assign an overall quality score:

| Overall Rating | Criteria |
|----------------|----------|
| **Excellent** | All dimensions rated "No Issues". Architecture ready for detailed design phase. |
| **Discrete** | At most 1 dimension has "Minor Issues". Excellent analysis with minor gaps. |
| **Sufficient** | 2-3 dimensions have "Minor Issues". Good foundation but needs refinement. |
| **Inadequate** | 1 dimension has "Major Issues" OR 4+ dimensions have "Minor Issues". Significant problems in approach. |
| **Unacceptable** | 2+ dimensions have "Major Issues". Fundamentally flawed analysis. |

---

## Response Comparison Methodology

When comparing two architecture responses:

### Step 1: Individual Assessment
Rate each response independently across all dimensions.

### Step 2: Prioritize Dimensions

- **Critical**: Problem Understanding, Solution Approach & Design
- **Important**: Trade-off Analysis, Scalability & NFRs
- **Nice-to-have**: Practicality & Implementability, Clarity & Communication, Completeness & Depth

### Step 3: Preference Ranking

| Score | Meaning |
|-------|---------|
| **+2** | Response A significantly better |
| **+1** | Response A somewhat better |
| **0** | Roughly equivalent |
| **-1** | Response B somewhat better |
| **-2** | Response B significantly better |

---

## Common Pitfalls to Avoid

### When Designing:
- Don't jump to solution without understanding problem
- Don't ignore trade-offs or present false dichotomies
- Don't forget non-functional requirements
- Don't over-engineer or under-engineer
- Don't skip failure mode analysis

### When Evaluating:
- Don't penalize appropriate complexity
- Don't expect perfect solutions (trade-offs exist)
- Don't ignore feasibility concerns
- Verify technical claims where possible

---

## Use Case Examples

**Perfect for evaluating**:
- System design proposals
- Architecture decision records (ADRs)
- Technical design documents
- High-level design discussions
- Scalability analyses
- Migration strategies

**Not ideal for**:
- Code implementation (use Coding Rubric)
- Documentation (use Technical Writing Rubric)
- Research papers (use Research Rubric)

---

## Version History

- **v1.0** - Initial comprehensive architecture rubric following coding rubric v1.1 format

---

*This rubric guide is designed for the AI Engineering Critique repository to demonstrate systematic evaluation methodology for AI-generated system architecture and design.*
