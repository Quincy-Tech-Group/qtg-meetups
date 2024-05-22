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
  response = client.images.generate(
      model="dall-e-3",
      prompt=args.prompt,
      # size="1024x1024",
      quality="standard",
      style='vivid',
      n=1,
  )

  image_url = response.data[0].url

  print(image_url)


if __name__ == "__main__":
  main()
