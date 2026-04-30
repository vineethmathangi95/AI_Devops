import ollama
import os
import shutil
import sys

IMAGE_NAME = "vineethmathangi95/python:ollama"
JAR_NAME = "app.jar"

PROMPT = """
You are a Docker expert.

Generate ONLY a Dockerfile for Java JAR app.

STRICT RULES:
- ONLY use this base image: eclipse-temurin:17-jdk
- NEVER change or invent base image names
- NEVER use openjdk or eclipse:*
- Copy app.jar
- Run: java -jar app.jar
- Expose port 8080
- Output ONLY Dockerfile (no markdown, no text)
"""


def clean_dockerfile(text):
    """
    Remove common LLM garbage like:
    'Here is your Dockerfile:' etc.
    """
    lines = text.split("\n")

    cleaned = []
    for line in lines:
        line_lower = line.lower().strip()

        # remove unwanted AI text
        if line_lower.startswith("here"):
            continue
        if "dockerfile" in line_lower and "from" not in line_lower:
            continue

        cleaned.append(line)

    return "\n".join(cleaned).strip()


def generate_dockerfile():
    response = ollama.chat(
        model='llama3.2:1b',
        messages=[{'role': 'user', 'content': PROMPT}]
    )
    return response['message']['content']


if __name__ == "__main__":

    # 1. Get jar path
    jar_path = input("Enter full path of your JAR file: ")

    # 2. Validate file exists
    if not os.path.exists(jar_path):
        print("❌ JAR file not found!")
        sys.exit(1)

    # 3. Copy + rename to app.jar
    shutil.copy(jar_path, JAR_NAME)
    print(f"\n✔ Copied as {JAR_NAME}")

    # 4. Generate Dockerfile using Ollama
    print("\nGenerating Dockerfile using Ollama...")
    raw_dockerfile = generate_dockerfile()
    dockerfile = clean_dockerfile(raw_dockerfile)

    # 5. Save Dockerfile
    with open("Dockerfile", "w") as f:
        f.write(dockerfile)

    print("\n✔ Dockerfile created!")

    # 6. Build Docker image
    print("\nBuilding Docker image...")
    build_status = os.system(f"docker build -t {IMAGE_NAME} .")

    if build_status != 0:
        print("❌ Docker build failed. Stopping.")
        sys.exit(1)

    # 7. Push image
    print("\nPushing image to Docker Hub...")
    push_status = os.system(f"docker push {IMAGE_NAME}")

    if push_status != 0:
        print("❌ Docker push failed.")
        sys.exit(1)

    print("\n🚀 DONE: Image built and pushed successfully!")
