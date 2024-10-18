from openai import OpenAI
import os
from dotenv import load_dotenv

# set up
env_path = os.path.join('..', '.env')
load_dotenv(dotenv_path=env_path)
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)
base_dir = '/Users/guobaichen/Documents/MyProgram/NTU-2024-spring-GenAI'

def generate_essay(mode, role):
    match mode:
        case "eng":
            topic_name = 'hw2/topics/english_topic.txt'
            topic_path = os.path.join(base_dir, topic_name)
            with open(topic_path, 'r') as f:
                topic = f.read()
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are a {role}."},
                    {"role": "user", "content": topic}
                ]
            )
            file_name = 'hw2/essays/english_essay.txt'
        case "zh":
            topic_name = 'hw2/topics/chinese_topic.txt'
            topic_path = os.path.join(base_dir, topic_name)
            with open(topic_path, 'r') as f:
                topic = f.read()
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"你是一名{role}."},
                    {"role": "user", "content": topic}
                ]
            )
            file_name = 'hw2/essays/chinese_essay.txt'
    reply = completion.choices[0].message.content
    # save essay
    file_path = os.path.join(base_dir, file_name)
    with open(file_path, 'w') as f:
        f.write(reply)
    return

def evalue_essay(mode):
    match mode:
        case "eng":
            # get evaluation rules
            evaluation_file_name = 'hw2/evaluation_rules/prompt_en.txt'
            evaluation_file_path = os.path.join(base_dir, evaluation_file_name)
            with open(evaluation_file_path, 'r') as f:
                evaluation_rules = f.read()

            # get student's essay
            essay_file_name = 'hw2/essays/english_essay.txt'
            essay_file_path = os.path.join(base_dir, essay_file_name)
            with open(essay_file_path, 'r') as f:
                essay = f.read()

            # evaluate
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": evaluation_rules},
                    {"role": "user", "content": f"Student's Essay: {essay}"}
                ]
            )
            file_name = 'hw2/evaluation_results/english_evaluation_result.txt'
        case "zh":
            # get evaluation_rules
            evaluation_file_name = 'hw2/evaluation_rules/prompt_zh.txt'
            evaluation_file_path = os.path.join(base_dir, evaluation_file_name)
            with open(evaluation_file_path, 'r') as f:
                evaluation_rules = f.read()

            # get student's essay
            essay_file_name = 'hw2/essays/chinese_essay.txt'
            essay_file_path = os.path.join(base_dir, essay_file_name)
            with open(essay_file_path, 'r') as f:
                essay = f.read()

            # evaluate
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": evaluation_rules},
                    {"role": "user", "content": f"學生的文章: {essay}"}
                ]
            )
            file_name = 'hw2/evaluation_results/chinese_evaluation_result.txt'
    reply = completion.choices[0].message.content
    # save evaluation
    file_path = os.path.join(base_dir, file_name)
    with open(file_path, 'w') as f:
        f.write(reply)
    return

def main():
    # generate english essay
    role = "perfect writer"
    generate_essay("eng", role)

    # evaluate english essay
    evalue_essay("eng")

    # generate chinese essay
    role = "專業的作家"
    generate_essay("zh", role)

    # evaluate chinese essay
    evalue_essay("zh")

if __name__ == '__main__':
    main()