import os
from pprint import pprint
import json
import argparse

from openai import OpenAI


# python demo_1_flashcards.py "american history involving spain"
# python demo_1_flashcards.py arithmatic --grade 7


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)



def _check_moderation(text):
  moderation = client.moderations.create(
    input=text,
  )
  result = moderation.results[0]
  if result.flagged:
    print(result)
    raise RuntimeError("Content flagged!")


def _get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('prompt', type=str)
  parser.add_argument('--grade',  type=int, default=4)
  args = parser.parse_args()
  return args



def main():

  args = _get_args()
  _check_moderation(args.prompt)
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": f"Give ten questions and answers. Give the answer using valid JSON. Use a 'questions' field that contains objects with 'question' and 'answer' fields. Responses should be for grade {args.grade}."},
      {"role": "user", "content": args.prompt}
    ]
  )

  content = completion.choices[0].message.content

  _check_moderation(content)

  results = json.loads(content)
  pprint(results)


if __name__ == "__main__":
  main()
