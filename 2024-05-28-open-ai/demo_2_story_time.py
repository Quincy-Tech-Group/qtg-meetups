import os
import argparse

from openai import OpenAI, Moderation


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def _get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('prompt', type=str)
  parser.add_argument('--grade',  type=int, default=4)
  parser.add_argument('--students',  type=str)
  args = parser.parse_args()
  return args


def _check_moderation(text):
  moderation = client.moderations.create(
    input=text,
  )
  result = moderation.results[0]
  if result.flagged:
    print(result)
    raise RuntimeError("Content flagged!")


def main():

  args = _get_args()
  _check_moderation(args.prompt)
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": f"Tell me a story using 5 paragraphs. Responses should be for grade {args.grade}. Include the following as characters in the story: {args.students}. The story should be funny and educational."},
      {"role": "user", "content": args.prompt}
    ]
  )

  content = completion.choices[0].message.content
  _check_moderation(content)
  print("")
  print(content)

if __name__ == "__main__":
  main()
