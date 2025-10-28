import subprocess
import os
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import re
import logging

def main():
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    config_dir = os.path.expanduser("~/.config/seek")
    env_path = os.path.join(config_dir, ".env")
    output_dir = os.path.join(config_dir, 'responses')
    load_dotenv(env_path)

    result = subprocess.run(
        [
            "zenity",
            "--entry",
            "--title=Ask a Question",
            "--text=What is your question?",
            "--width=800",
            "--height=200",
        ],
        capture_output=True,
        text=True,
    )
    exit() if result.returncode != 0 else None
    question = result.stdout.strip()
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    logging.info(f'User Input \n{question}')

    prompt = (
        "You are a helpful assistant."
        "Keep answers short, clear, and in markdown format."
        "This is intended as a one off, so give as much background information as posible while maintaining length of response"
        "At the top of every response, include a specific 2 word title separated by an underscore _ inside '{}'"
        "The title will be used as a filename, so ensure it exists and is in suitable format."
        "There can be no spaces in the title under any circumstances."
    ) + question

    provider = os.getenv("AI_PROVIDER")
    api_key = os.getenv("AI_API_KEY")
    
    if provider == "anthropic":
        llm = ChatAnthropic(
            model = "claude-sonnet-4-5-20250929",
            api_key=api_key
        )
    elif provider == "deepseek":
        llm = ChatOpenAI(
            model = 'deepseek-chat',
            api_key=api_key,
            base_url='https://api.deepseek.com'
        )
    else:
        llm = ChatOpenAI(
            model="gpt-4",
            api_key=api_key
        )

    try:
        response = llm.invoke(prompt).content

        logging.info(f'response \n{response}')
        match = re.search(pattern=r"\{([^{}]+)\}", string=response)
        if match:
            title = match.group(1)
            output_file = os.path.join(output_dir, f"{title}.md")
        else:
            output_file = os.path.join(output_dir, f"{timestamp}.md")

        logging.info(f'Output Filenamme \n{output_file}')

        with open(output_file, "w") as f:
            f.write(f"# Question\n\n{question}\n\n# Response\n\n{response}")
        subprocess.run(["kitty", "nvim", output_file])
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
