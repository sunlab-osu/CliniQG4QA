import json
import uuid
import re


def prune_sentence(sent):
    sent = sent.replace("_", " ")
    sent = sent.replace("&lt;", "<")
    sent = sent.replace("&gt;", ">")
    sent = sent.replace("&amp;", "&")
    sent = sent.replace("&quot;", "\"")
    sent = sent.replace("& quot ;", "\"")
    sent = sent.replace("&nbsp;", " ")
    sent = sent.replace("&apos;", "\'")
    sent = sent.replace("& apos ;", "\'")
    sent = sent.replace("_", "")
    sent = sent.replace("\"", "")

    # remove whitespaces before punctuations
    sent = re.sub(r'\s([?.!\',)"](?:\s|$))', r'\1', sent)
    # remove multiple punctuations
    sent = re.sub(r'[?.!,]+(?=[?.!,])', '', sent)
    return sent


def clean_datasets(filename='data.json'):
    with open(filename, 'r') as f:
        data = json.load(f)

    new_json = dict()
    new_json["version"] = "1.1"
    new_json["data"] = list()
    # Data level
    for i in range(len(data["data"])):
        actual_data = data["data"][i]
        new_data = dict()
        new_data["title"] = actual_data["title"]
        new_data["paragraphs"] = list()
        # Paragraph level
        for j in range(len(actual_data["paragraphs"])):
            new_paragraph = dict()
            temp_list = actual_data["paragraphs"][j]["context"]
            # remove whitespaces between texts and punctuations
            context = " ".join((" ".join(temp_list).split()))

            context = prune_sentence(context)
            context = " ".join(context.split())
            context = context.lower()
            new_paragraph["context"] = context
            new_paragraph["qas"] = list()
            qas = actual_data["paragraphs"][j]["qas"]
            if len(qas) == 0:
                # print('No QAS for this note')
                continue
            # QAS Level
            for k in range(len(qas)):
                new_qas = dict()
                new_qas["answers"] = list()
                answers = qas[k]["answers"]
                # Answers level
                for l in range(len(answers)):
                    if answers[l]["answer_entity_type"] == 'complex':
                        continue
                    new_answers = dict()
                    entity = answers[l]["text"]
                    if entity != "":
                        entity = " ".join(entity.split())
                        while entity[-1] in [',', '.', '?', '!','-']:
                                entity = entity[:-1]
                    entity = prune_sentence(entity)
                    entity = " ".join(entity.split())
                    entity = entity.lower()
                    
                    evidence = answers[l]["evidence"]
                    evidence = " ".join(evidence.split())

                    evidence = prune_sentence(evidence)

                    evidence = " ".join(evidence.split())
                    evidence = evidence.lower()
                    if evidence:
                        while evidence[-1] in [',', '.', '?', '!','-']:
                            evidence = evidence[:-1]
                        # for b in range(len(evidence)):
                        char_pos = -1
                        temp_evidence = evidence
                        final_evidence = temp_evidence
                        num = 0
                        while char_pos == -1:
                            char_pos = context.find(temp_evidence)
                            final_evidence = temp_evidence
                            temp_evidence = ' '.join(temp_evidence.split()[:-1])
                            num += 1
                        if char_pos > 0 and final_evidence:
                            new_answers["answer_start"] = char_pos
                            new_answers["text"] = final_evidence
                            new_answers["entity"] = entity
                            new_qas["answers"].append(new_answers)
                        else:
                            continue

                questions = qas[k]["question"]
                # new_qas["question"] = list()
                new_answers = new_qas['answers']
                if len(new_answers) == 0:
                    # print("No answers for questions.")
                    continue
                for p in range(len(questions)):
                    new_qas = dict()
                    question = questions[p]
                    question = prune_sentence(question)
                    question = " ".join(question.split())
                    question = question.lower()
                    new_qas["question"] = question
                    new_qas["id"] = str(uuid.uuid1().hex)
                    new_qas['answers'] = new_answers
                    new_qas["question_type"] = questions[p].split(" ")[0]
                    new_paragraph["qas"].append(new_qas)

            new_data["paragraphs"].append(new_paragraph)
        new_json["data"].append(new_data)

    return new_json


def double_check_processed_data(new_json):
    question_num = 0
    context_num = 0
    qa_pair_num = 0

    for subset in new_json['data']:
        print('#' * 50)
        print('Check', subset['title'])
        subset_question_num = 0
        subset_context_num = 0
        subset_qa_pair_num = 0
        for para in subset['paragraphs']:
            context_num += 1
            subset_context_num += 1

            assert para['context']
            assert len(para['qas']) > 0
            for qa in para['qas']:
                question_num += 1
                subset_question_num += 1

                assert qa['question']
                assert id
                assert len(qa['answers']) > 0
                for answer in qa['answers']:
                    qa_pair_num += 1
                    subset_qa_pair_num += 1
                    assert isinstance(answer['answer_start'], int)
                    assert answer['answer_start'] > 0
                    assert answer['text']

        print('Note (context): {}, Questions: {}, QA_pair: {}'.format(subset_context_num, subset_question_num,
                                                                      subset_qa_pair_num))

    print('#' * 50)
    print('Total Statistics:')
    print('Note (context): {}, Questions: {}, QA_pair: {}'.format(context_num, question_num, qa_pair_num))


def save_json(json_data, output='data_preprocessed.json'):
    print('Saving file...')
    with open(output, 'w') as f:
        json.dump(json_data, f)


def split_datasets_into_subsets(dataset_json, output_dir='../emrQG/', max_answer_length=30):
    # split the dataset into three subsets: medication, relations, risk
    # remove the answers whose lengths are larger than max_answer_length (token)
    subsets=[]
    for subset in dataset_json['data']:
        print('Split', subset['title'])
        data = []
        for para in subset['paragraphs']:
            subdata = {"title": '', 'paragraphs': []}
            new_para = {'context': para['context'], 'qas': []}
            for qa in para['qas']:
                new_answers = []
                for answer in qa['answers']:
                    answer_length = len(answer['text'].split())
                    if answer_length < max_answer_length:
                        new_answers.append(answer)
                if len(new_answers) > 0:
                    new_qa = {'question': qa['question'], 'id': qa['id'], 'answers': new_answers, 'question_type' : qa['question_type'].lower()}
                    new_para['qas'].append(new_qa)

            subdata['paragraphs'].append(new_para)
            subdata['title'] = ' '.join(new_para['context'].split()[:2])
            data.append(subdata)
        subset_json = {'data': data, 'version': 1.1}
        json.dump(subset_json, open(output_dir + subset['title'] + '.json', 'w'))
        subsets.append(subset_json)
    return subsets


def show_dataset_statistics(data_json,dataset_name):
    print('#' * 50)
    print(dataset_name)
    note_num = len(data_json['data'])
    question_num = 0
    qa_pair_num = 0
    for paras in data_json['data']:
        for para in paras['paragraphs']:
            for qa in para['qas']:
                question_num += 1
                qa_pair_num += len(qa['answers'])

    print('Note (context): {}, Questions: {}, QA_pair: {}'.format(note_num, question_num, qa_pair_num))


if __name__ == '__main__':
    print("begin cleaning...")
    new_json = clean_datasets(filename='../emrQG/data.json')
    print('checking the processed data')
    double_check_processed_data(new_json)
    # save_json(new_json, output='data_preprocessed.json')
    print('splitting the datasets and pruning answers...')
    subsets=split_datasets_into_subsets(new_json, output_dir='../emrQG/', max_answer_length=20)
    print('After pruning answers...')
    subset_name=['medication','relation','risk']
    for i, subset in enumerate(subsets):
        show_dataset_statistics(subset,subset_name[i])