import subprocess
import os
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import re
import argparse


#!/usr/bin/env python3
"""
Seek - A command-line AI assistant tool
Usage:
    seek -sp filename.txt
    seek -q "Your question here" --system_prompt custom.txt
"""

def parse_args():
    parser = argparse.ArgumentParser(description="Process a question for the AI model.")
    parser.add_argument('-sp', type=str, metavar="FILE", help='The system prompt to guide the AI model.', default="~/.config/seek/system_prompt.txt")
    parser.add_argument("-q", type=str, help="The question to be processed by the AI model.")
    return parser.parse_args()

def main():
    args = parse_args()
    question = args.q
    filepath = args.sp

    question = args.question
    system_prompt = filepath.read_text().strip()

    config_dir = os.path.expanduser("~/.config/seek")
    env_path = os.path.join(config_dir, ".env")
    output_dir = os.path.join(config_dir, "responses")

    load_dotenv(env_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    prompt = system_prompt + question
    
    try:
        provider = os.getenv("AI_PROVIDER")
        api_key = os.getenv("AI_API_KEY")
    except Exception as e:
        print(f"No Provider or API Key found")
        return 1

    if provider == "anthropic":
        llm = ChatAnthropic(model="claude-sonnet-4-5-20250929", api_key=api_key)
    elif provider == "deepseek":
        llm = ChatOpenAI(
            model="deepseek-chat", api_key=api_key, base_url="https://api.deepseek.com"
        )
    else:
        llm = ChatOpenAI(model="gpt-4", api_key=api_key)
    try:
        response = llm.invoke(prompt).content
        match = re.search(pattern=r"\{([^{}]+)\}", string=response)
        if match:
            title = match.group(1)
            output_file = os.path.join(output_dir, f"{title}.md")
        else:
            output_file = os.path.join(output_dir, f"{timestamp}.md")
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, "w") as f:
            f.write(response)
        print(f"{output_file}")
    except Exception as e:
        print(f"Error: {e}")
        return 1 
    return 0

if __name__ == "__main__":
    main()
