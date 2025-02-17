import openai
import os
# Set your OpenAI API key
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

#openai.api_key = settings.openai_api_key
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()




def generate_context(context_of_person,context_of_documentation,addition_misc_data):
    messages = [
        {
            "role": "system",
            "content": "You are a healthcare AI assistant that provides accurate and concise responses based on healthcare coverage data. Use the document data and personal info to answer questions effectively. If the answer is not in the data, state so."
        },
        {
            "role": "user",
            "content": "### PERSONAL DATA ###\n" + context_of_person
        },        
        {
            "role": "user",
            "content": "### DOCUMENT DATA ###\n" + context_of_documentation
        },
        {
            "role": "user",
            "content": "### ADDITIONAL INFO ###\n" + addition_misc_data
        },        
    ]
    return messages

def formulate_question_or_task(messages,questions_or_task):
    messages.append({
        "role": "user",
        "content": "### QUESTIONS OR TASKS ###\n" + questions_or_task
    })
    return messages





def get_openai_response(formatted_prompt):
    # Generate response
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=formatted_prompt#[
        #    {"role": "developer", "content": "You are a helpful assistant."},
        #    {"role": "user", "content": prompt}
        #]
    )
    return response.choices[0].message



if __name__ == "__main__":
    prompt = "Write a haiku about recursion in programming."
    get_openai_response(full_prompt_prompt)
    print(completion.choices[0].message)


