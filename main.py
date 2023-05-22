import eel
import requests
import json
import os

eel.init('web') 

@eel.expose
def send_message_to_gpt4(initial_prompt):
    endpoint = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': 'Bearer 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'
    }
    
    # 1. Refine the initial prompt
    data = {
        'model': 'gpt-4',
        'messages': [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Refine my initial inquiry/request, {initial_prompt}, to ensure that it is specific, clear, and concise to set a strong foundation for subsequent interactions with ChatGPT-4. Do not write an introduction, a conclusion, or any explanation, just provide the inquiry/request/question in a refined way."}
        ]
    }
    print("Sending data:", data) 
    response = requests.post(endpoint, headers=headers, json=data)
    print("Status code:", response.status_code)
    try:
        print("Response:", response.json())
    except Exception as e:
        print("Failed to parse response as JSON:", e)

    try:
        refined_prompt = response.json()['choices'][0]['message']['content']
    except KeyError:
        print("Failed to extract 'choices' from response")
        refined_prompt = "Default refined prompt"

    # 2. Generate prompt suggestions
    data['messages'].append({"role": "user", "content": f"Please provide me with the top five prompts that I could ask ChatGPT in order to achieve to best response to {refined_prompt}. Do not write an introduction, a conclusion, or any explanation, just provide the prompts in a list format."})
    print("Sending data:", data) 
    response = requests.post(endpoint, headers=headers, json=data)
    prompt_suggestions = response.json()['choices'][0]['message']['content']
    print("Prompt Suggestions:", prompt_suggestions) 

    # 3. Respond to the refined prompt with consideration of the prompt suggestions
    data['messages'].append({"role": "user", "content": f"Respond to {refined_prompt}. Within your answer, consider responses to {prompt_suggestions}"})
    print("Sending data:", data) 
    response = requests.post(endpoint, headers=headers, json=data)
    gpt_refined_prompt_answer = response.json()['choices'][0]['message']['content']
    print("GPT-4's Response to Refined Prompt:", gpt_refined_prompt_answer) 


    # 4. Evaluate the response
    data['messages'].append({"role": "user", "content": f"Evaluate whether {gpt_refined_prompt_answer} provides an adequate answer to {initial_prompt} and {refined_prompt} and state how {gpt_refined_prompt_answer} could be improved."})
    print("Sending data:", data) 
    response = requests.post(endpoint, headers=headers, json=data)
    feedback = response.json()['choices'][0]['message']['content']
    print("Evaluation and Feedback:", feedback) 


    # 5. Implement the feedback to create an improved version of the response
    data['messages'].append({"role": "user", "content": f"Implement the feedback from {feedback} to create an improved version of {gpt_refined_prompt_answer}. Do not write an introduction, a conclusion, or any explanation, just provide the new response to {initial_prompt} and {refined_prompt}"})
    print("Sending data:", data) 
    response = requests.post(endpoint, headers=headers, json=data)
    final_response = response.json()['choices'][0]['message']['content']
    print("Final Improved Response:", final_response) 


    return final_response

eel.start('index.html')
