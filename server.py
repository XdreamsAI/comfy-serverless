import runpod
import json
import subprocess
import base64
import os

# Path to workflow file
WORKFLOW_PATH = "/workspace/workflow.json"

def handler(event):
    """Main handler for RunPod Serverless"""

    # Input data from the request
    input_data = event.get("input", {})

    # Save input JSON into a runtime workflow file
    runtime_workflow_path = "/workspace/runtime_workflow.json"
    with open(WORKFLOW_PATH, "r") as f:
        workflow = json.load(f)

    # Insert prompt into workflow (basic example)
    prompt = input_data.get("prompt", "Hello from ComfyUI Serverless")
    workflow["prompt"] = prompt

    with open(runtime_workflow_path, "w") as f:
        json.dump(workflow, f)

    # Run ComfyUI in headless mode
    run_command = [
        "python3",
        "/workspace/ComfyUI/main.py",
        "--workflow", runtime_workflow_path,
        "--output-dir", "/workspace/output"
    ]

    subprocess.run(run_command, check=True)

    # Find generated file
    output_files = os.listdir("/workspace/output")
    if not output_files:
        return {"error": "No output generated"}

    output_path = "/workspace/output/" + output_files[-1]

    # Encode image to base64 so RunPod can return it
    with open(output_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    return {
        "image_base64": encoded
    }

# Start RunPod serverless handler
runpod.serverless.start({"handler": handler})
