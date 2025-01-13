import json
with open('data/goodui_answer.json', 'r') as f:
    answer = json.load(f)

with open('gpt_results.json', 'r') as f:
    gpt_results = json.load(f)

answer_list = [a['answer_num'] for a in answer]
print(answer_list)

result_list = [0] * len(answer_list)
for result in gpt_results:
    result_list[int(result['folder'])] = int(result['answer_num'])
print(result_list)

correct = 0
for i in range(len(answer_list)):
    if answer_list[i] == result_list[i]:
        correct += 1

print(f'Correct: {correct}/{len(answer_list)}')