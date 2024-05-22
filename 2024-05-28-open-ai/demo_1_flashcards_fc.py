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


def _get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('prompt', type=str)
  parser.add_argument('--grade',  type=int, default=4)
  parser.add_argument('--num-questions',  type=int, default=5)
  args = parser.parse_args()
  return args


GET_QA_FUNCTION = {
  "name": "generate_questions_and_answers",
  "description": "Generate a list of questions and their answers "
                 "for a given topic.",
  "parameters": {
      "type": "object",
      "properties": {
          "questions": {
              "type": "array",
              "items": {"type": "string"}
          },
          "answers": {
              "type": "array",
              "items": {"type": "string"}
          }
      },
      "required": ["questions", "answers"]
  }
}

def main():

  args = _get_args()

  response = client.chat.completions.create(
      model="gpt-4",
      messages=[
          {"role": "system",
           "content": f"You are a helpful assistant. Responses should be for "
                      f"grade level {args.grade}."},
          {"role": "user",
           "content": f"Generate {args.num_questions} questions and answers "
                      f"for the following topic: {args.prompt}"}
      ],
      functions=[GET_QA_FUNCTION],
      function_call={"name": "generate_questions_and_answers"}
  )

  content_json = response.choices[0].message.function_call.arguments
  content = json.loads(content_json)

  results = [
      {"question": q, "answer": a}
      for q, a in zip(content["questions"], content["answers"])
  ]

  pprint(results)


if __name__ == "__main__":
  main()
