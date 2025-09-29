import os
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv()

client = Cerebras(
  api_key=os.environ.get("CEREBRAS_API_KEY"),
)

def main():
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user", 
                "content": "Why is fast inference important?"
            }
        ],
        model="llama-4-scout-17b-16e-instruct",
    )
    print(chat_completion)

if __name__ == "__main__":
    main()