import os
from pprint import pprint
import json
import argparse

from openai import OpenAI


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def main():
  args = _get_args()
  _check_moderation(args.prompt)
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": f"Give ten questions and answers. Give the "
                                    f"answer using valid JSON. Use a "
                                    f"'questions' field that contains objects "
                                    f"with 'question' and 'answer' fields. "
                                    f"Responses should be for grade "
                                    f"{args.grade}."},
      {"role": "user", "content": args.prompt}
    ]
  )

  content = completion.choices[0].message.content

  _check_moderation(content)

  results = json.loads(content)
  pprint(results)


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


if __name__ == "__main__":
  main()
