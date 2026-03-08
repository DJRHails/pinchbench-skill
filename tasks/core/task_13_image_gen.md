---
id: task_13_image_gen
name: AI Image Generation
category: creative
grading_type: llm_judge
timeout_seconds: 120
multimodal_judge: true
judge_artifacts:
  - path: "robot_cafe.png"
    type: image
    label: "Generated image"
workspace_files: []
---

## Prompt

Generate an image of a friendly robot sitting in a cozy coffee shop, reading a book. Save it as "robot_cafe.png" in the current directory.

## Expected Behavior

The agent should:

1. Use any available image generation capability (bash script, tool, or API) to create an image matching the description
2. Provide a descriptive prompt that captures the key elements: robot, coffee shop setting, cozy atmosphere, reading a book
3. Save the generated image to the specified filename "robot_cafe.png"
4. Confirm successful generation and describe what was created

This tests the agent's ability to:

- Utilize available image generation capabilities appropriately
- Craft effective image prompts from natural language descriptions
- Handle file output operations for generated content
- Communicate results clearly to the user

## Grading Criteria

- [ ] An image was generated and saved as robot_cafe.png
- [ ] The image depicts a robot in a coffee shop / cafe setting
- [ ] The image shows the robot reading a book
- [ ] The image is well-composed and aesthetically pleasing
- [ ] Agent confirmed successful generation

## LLM Judge Rubric

### Criterion 1: Image Content (Weight: 40%)

Evaluate the generated image visually. The image artifact is attached.

**Score 1.0**: Image clearly depicts a friendly robot in a coffee shop or cafe setting, reading a book. All three core elements (robot, cafe, book) are present and recognizable.
**Score 0.75**: Image contains all three elements but one is less prominent or partially obscured.
**Score 0.5**: Image contains a robot and one other requested element (cafe or book), but is missing one core element.
**Score 0.25**: Image only loosely relates to the request — e.g. just a robot with no cafe or book context.
**Score 0.0**: No image was generated, the image file is missing, or the image is completely unrelated to the request.

### Criterion 2: Image Quality (Weight: 30%)

**Score 1.0**: Image is well-composed, detailed, and aesthetically pleasing. Colors, lighting, and composition create a cohesive scene.
**Score 0.75**: Image is decent quality with minor aesthetic issues (e.g. slightly awkward composition, minor artifacts).
**Score 0.5**: Image is recognizable but has noticeable quality issues (artifacts, poor composition, inconsistent style).
**Score 0.25**: Image is low quality, blurry, or has significant visual artifacts.
**Score 0.0**: No image generated or image is unviewable.

### Criterion 3: Task Execution (Weight: 20%)

**Score 1.0**: Image file was saved as `robot_cafe.png` in the workspace. Agent confirmed successful generation.
**Score 0.75**: Image was saved with a slightly different name but agent confirmed generation.
**Score 0.5**: Image was generated but not saved to the correct location, or agent did not confirm.
**Score 0.25**: Agent attempted image generation but the process failed or the file is missing.
**Score 0.0**: Agent did not attempt image generation.

### Criterion 4: Prompt Quality (Weight: 10%)

**Score 1.0**: Agent crafted a descriptive prompt capturing all key elements (friendly robot, cozy coffee shop, reading a book) with helpful artistic details.
**Score 0.75**: Prompt includes all main elements but is relatively bare.
**Score 0.5**: Prompt captures some elements but misses important details from the request.
**Score 0.25**: Prompt is too vague or misses multiple key elements.
**Score 0.0**: No prompt was visible in the transcript.

## Additional Notes

- The agent may use any available image generation method — bash scripts (e.g. nano-banana-pro), built-in tools, or direct API calls
- Grading evaluates the output (the image) not the method used
- The multimodal judge will receive the generated image as an artifact for visual evaluation
- Creativity in prompt crafting is encouraged as long as it stays true to the core request
