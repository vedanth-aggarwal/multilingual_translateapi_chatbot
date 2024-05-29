import openai
from google.cloud import translate_v2 as translate
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'google.json'
# Set up your API keys
#openai.api_key = 
translate_client = translate.Client()

def translate_text(target, text):
    # Translates text into the target language
    result = translate_client.translate(text, target_language=target)
    return result['translatedText']

def detect_language(text):
    # Detects the language of the input text
    result = translate_client.detect_language(text)
    return result['language']

def get_openai_response(prompt):
    # Generates a response using OpenAI GPT API
    '''
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
    '''
    from openai import OpenAI

    client = OpenAI(api_key='')

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        #stream=True,
    )
    return stream.choices[0].message.content
    #for chunk in stream:
    #    if chunk.choices[0].delta.content is not None:
    #        print(chunk.choices[0].delta.content, end="")

def main():
    # Accept user input
    user_input = input("Please enter your question: ")

    # Detect the language of the input text
    input_language = detect_language(user_input)
    
    # Translate the input text to English
    translated_input = translate_text('en', user_input)

    # Get the OpenAI response to the translated input
    openai_response = get_openai_response(translated_input)

    # Translate the OpenAI response back to the original language
    translated_output = translate_text(input_language, openai_response)

    # Output the translated response
    print(f"Answer: {translated_output}")

if __name__ == "__main__":
    main()
