#!/usr/bin/env python3
import subprocess
import os
from datetime import datetime
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import re

load_dotenv()

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "docs")
os.makedirs(output_dir, exist_ok=True)


result = subprocess.run(
    [
        "zenity",
        "--entry",
        "--title=Ask a Question",
        "--text=What is your question?",
        "--width=800",
        "--height=400",
    ],
    capture_output=True,
    text=True,
)

exit() if result.returncode != 0 else None

question = result.stdout.strip()
timestamp = datetime.now().strftime("%Y%m%d%H%M")

print(question)

prompt = (
    "You are a helpful assistant, answering questions about coding in a python3, linux mint, i3wm environment."
    "Keep answers short, clear, and in markdown format."
    "At the top of every response, include a specific 2 word title separated by an underscore _ inside '{}'"
    "The title will be used as a filename, so ensure it exists and is in suitable format.\n\n"
) + question

llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0.5,
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

try:
    response = llm.invoke(prompt).content
    match = re.search(pattern=r"\{([^{}]+)\}", string=response)
    if match:
        title = match.group(1)
        output_file = os.path.join(output_dir, f"{title}.md")
    else:
        output_file = os.path.join(output_dir, f"{timestamp}.md")

    with open(output_file, "w") as f:
        f.write(f"# Question\n\n{question}\n\n# Response\n\n{response}")

    subprocess.run(["alacritty", "-e", "nvim", output_file])
except Exception as e:
    print(f"Error: {e}")

# End of script
