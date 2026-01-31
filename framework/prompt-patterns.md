# Prompt Patterns

Effective patterns for getting high-quality outputs from LLMs.

## 1. Persona Pattern
Assigns a specific role to the AI to tailor the tone and perspective.
**Example**: "Act as a Senior Principal Engineer at Google..."

## 2. Few-Shot Prompting
Providing examples of input-output pairs to guide the model.
**Example**:
Input: "Fix this bug." -> Output: [Detailed fix]
Input: "Optimize this." -> Output: [Optimized code]

## 3. Chain of Thought
Encouraging the model to explain its reasoning before giving the final answer.
**Why**: Reduces logic errors in complex tasks.
**Example**: "Think step by step. First explain your plan, then write the code."

## 4. Templating
Using a standard structure for repetitive tasks.
**Example**: "Use the following format: ## Summary, ## Details, ## Conclusion."

## 5. Constraint Specification
Explicitly stating what the model should NOT do.
**Example**: "Do not use external libraries. Stick to the standard library."
