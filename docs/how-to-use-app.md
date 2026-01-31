# How to Use the App

## 1. Navigating the Interface
The sidebar allows you to switch between three main modes:
- **Generate & Evaluate**: The core workflow.
- **Prompt Analysis**: Improve your prompts before generating.
- **Rubric Builder**: Create custom evaluation criteria.

## 2. Generate & Evaluate Workflow
1. **Enter Prompt**: Type your request in the text area.
2. **Select Model**: Choose between available Claude models.
3. **Generate**: Click the button to get two distinct responses. *(Requires API Key)*
4. **Select Rubric**: Choose a pre-defined rubric (e.g., Code Review) or one you created.
5. **Score**: Use the sliders to rate both responses on each dimension.
6. **Calculate**: View the final weighted scores to see which response is better.

## 3. Improving Prompts
1. Go to **Prompt Analysis**.
2. Paste your draft prompt.
3. Click **Analyze**.
4. Review the suggestions and apply them to your prompt for better results.

## 4. Creating Rubrics
1. Go to **Rubric Builder**.
2. Edit the YAML definition to define your dimensions and weights.
3. Ensure weights sum to 1.0 (or appropriate scale).
4. Save the rubric. It will now be available in the Evaluation dropdown.
