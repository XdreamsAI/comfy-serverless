FROM runpod/comfyui:latest

# Copy workflow and server files
COPY workflow.json /workspace/workflow.json
COPY server.py /workspace/server.py

# Install extra dependencies
COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# Set the entrypoint
CMD ["python3", "/workspace/server.py"]
