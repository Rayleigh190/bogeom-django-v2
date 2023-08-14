import os
import openai

OPENAI_KEY = os.environ.get("OPENAI_KEY")


def chatGPT(ocr_result): # cahtGPT API
  openai.api_key = OPENAI_KEY
  try:
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "user",
          "content": str(ocr_result) + "Extract one product name from this list. Also tell me the index of that element. Respond in the following JSON format. {\"index\": number,\"product_name\":\"product name\"} . If extraction fails, respond with: {\"product_name\":\"fail\"}"
        }
      ],
    )
  except Exception as e:
    print('ChatGPT 예외가 발생했습니다.', e)

  decoded = completion.choices[0].message["content"]
  return decoded