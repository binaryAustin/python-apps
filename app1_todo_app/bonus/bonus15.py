import json

with open("bonus/questions.json", "r", encoding="utf8") as fr:
    content = fr.read()


data = json.loads(content)
user_choices: dict[str, int] = {}
score = 0

length = len(data["questions"])

for question in data["questions"]:
    print(question["question_text"])
    for index, alternative in enumerate(question["alternatives"]):
        print(f"{index + 1}.{alternative}")
    user_choice = int(input("Enter your answer: "))
    user_choices[str(question["id"])] = user_choice
    if user_choice == question["correct_answer"]:
        score += 1

print(f"Score: {score}/{length}")

for question in data["questions"]:
    question_id = question["id"]
    correct_answer = question["correct_answer"]
    message = f"Question {question_id}. User choice: {user_choices[str(question_id)]}. Correct answer: {correct_answer}"
    print(message)
