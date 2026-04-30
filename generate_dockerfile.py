import ollama
import os
import shutil

IMAGE_NAME = "vineethmathangi95/python:ollama"

PROMPT = """
Generate ONLY a Dockerfile for a Java JAR application.

Requirements:
- Use OpenJDK light weight image
- Copy app.jar into container
- Run: java -jar app.jar
- Expose port 8080
"""

def generate_dockerfile():
    response = ollama.chat(
        model='llama3.1:1b',
        messages=[{'role': 'user', 'content': PROMPT}]
    )
    return response['message']['content']


if __name__ == "__main__":

    # 1. Get jar path
    jar_path = input("Enter full path of your JAR file: ")

    # 2. Copy jar locally
    shutil.copy(jar_path, "app.jar")

    # 3. Generate Dockerfile
    dockerfile = generate_dockerfile()

    with open("Dockerfile", "w") as f:
        f.write(dockerfile)

    print("\nDockerfile created!")

    # 4. Build image
    print("\nBuilding Docker image...")
    os.system(f"docker build -t {IMAGE_NAME} .")

    # 5. Push image to Docker Hub
    print("\nPushing image to Docker Hub...")
    os.system(f"docker push {IMAGE_NAME}")

    print("\nDONE 🚀 Image built and pushed successfully!")
