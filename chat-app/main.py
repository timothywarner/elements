import os
from dotenv import load_dotenv
import openai
import textwrap
import time

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple in-memory cache
name_cache = {}


def get_name_description(name):
  """
  Retrieve the etymology and meaning of a given baby name.

  Args:
    name (str): The baby name to retrieve the description for.

  Returns:
    str: The etymology and meaning of the baby name.
  """
  if name in name_cache:
    return name_cache[name]

  prompt = f"Describe the etymology and meaning of the baby name {name}"

  response = openai.Completion.create(
    engine="gpt-3.5-turbo",
    prompt=prompt,
    max_tokens=100,  # Adjust max tokens as needed
    n=1,
    stop=None,
    temperature=0.7,  # Tweak temperature for creativity
  )

  # Store result in cache
  name_cache[name] = response.choices[0].text.strip()
  return name_cache[name]


def main():
  """
  Main function to interact with the Zoltar baby name expert.

  This function prompts the user to enter a baby name and retrieves
  the etymology and meaning of the name using the OpenAI GPT-3 model.
  The description is then printed to the console.
  """
  print("Welcome to Zoltar, your baby name expert!")
  while True:
    name = input("Enter a baby name (or 'quit' to exit): ")
    if name.lower() == "quit":
      break

    # Wait a second before the API call (rate limiting)
    time.sleep(1)

    description = get_name_description(name)
    print("\n" + textwrap.fill(description, width=70) + "\n")


if __name__ == "__main__":
  main()
