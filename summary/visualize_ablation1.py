import json
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

import xml.etree.ElementTree as ET
import ast

#############################################################################################################
#### Helper functions                                                                                    ####
#############################################################################################################
def append_root_tags(string):
    if not string.strip().startswith("<root>"):
        string = "<root>\n" + string
    if not string.strip().endswith("</root>"):
        string += "\n</root>"
    return string

def parse_xml_to_dict(xml_string: str):
    """Parse the XML string to a dictionary.

    :param xml_string: The XML string to parse.
    :return: A tuple of (output, reasoning).
    """
    # Append root tags if necessary
    # print(xml_string)
    xml_string = append_root_tags(xml_string)

    # remove comments
    remove_comment_func = lambda string: string.split('//')[0].rstrip() if '//' in string else string
    xml_string = '\n'.join(remove_comment_func(line) for line in xml_string.split('\n'))
    
    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Find the 'final_answer' tag
    final_answer_element = root.find('final_answer')

    # Find the 'reasoning' tag
    reasoning = root.find('reasoning').text.strip()

    # Convert the 'final_answer' tag to a dictionary
    output = ast.literal_eval(final_answer_element.text.strip())
    # print(reasoning_element.text)
    return output, reasoning


def select_func(x):
    if isinstance(x, list):
        return x[0]
    elif isinstance(x, dict):
        return x.get('correctness', 'failed')
    else:
        return x


def calculate_accuracy(expr_result):
    file = expr_result['file']
    model_name = expr_result['model']
    problem_name = expr_result['problem']
    difference = expr_result.get('difference', 0)
    correct_len = min(100, 100 + 10 * difference)
    correct = expr_result['correct'][-correct_len:]
    origin_level_correctness = [correct[i:i+10] for i in range(0, len(correct), 10)]
    
    assert len(origin_level_correctness) == min(10, 10 + difference), f'Incorrect number of levels for {model_name} on {problem_name} with {difference} difference'
    filter_failed = lambda x: [y for y in x if y != 'failed']
    level_correctness = [filter_failed(x) for x in origin_level_correctness]
    failed_expr = [10 - len(x) for x in level_correctness]
    failed_num = sum(failed_expr)
    failed_expr = [x / 10 for x in failed_expr]
    if failed_num > 0:
        print(f'{model_name} on {problem_name} has {failed_num} failed results')
    level_accuracy = []
    for x in level_correctness:
        if len(x) == 0:
            level_accuracy.append(0)
        else:
            level_accuracy.append(sum(x) / 10)
    return {
        'model': model_name,
        'problem': problem_name,
        'difference': difference,
        'accuracy': level_accuracy,
        'failed': failed_expr,
        'level_correctness': origin_level_correctness
    }


#############################################################################################################
#### Load the results                                                                                    ####
#############################################################################################################

def load_results(RESULT_DIR):
    model_performance = []
    for file in os.listdir(RESULT_DIR):
        if file.endswith('.json'):
            # print(file)
            split_filename = file.split('_')
            model = split_filename[0]
            problem = split_filename[1]
            difference = int(split_filename[-1].split('.')[0])

            with open(RESULT_DIR + '/' + file) as f:
                correct = []
                for line in f.readlines()[-1:]:
                    data = json.loads(line)
                    for x in data:
                        correctness = select_func(x.get('correctness', 'failed'))
                        if not isinstance(correctness, bool): 
                            correctness = 'failed'
                        # the output can be a string or a dictionary
                        if (not correctness) and (not isinstance(x.get('output', None), dict)):
                            # if it is a string, try to parse it to a dictionary
                            # reusing the parse_xml_to_dict function
                            # if it fails, then the case is actually failed
                            if isinstance(x.get('output', None), str):
                                try:
                                    output, _ = parse_xml_to_dict(x.get('output', None))
                                    if not isinstance(output, dict):
                                        correctness = 'failed'
                                except:
                                    correctness = 'failed'
                        correct.append(correctness)
                performance = {
                    'model': model,
                    'problem': problem,
                    'correct': correct,
                    'difference': difference,
                    'file': file
                }
                model_performance.append(performance)
    return model_performance

#############################################################################################################
#### Aggregate the results                                                                               ####
#############################################################################################################

RESULT_DIR = 'Results_fewshot/MFP_self_close/'
model_performance = load_results(RESULT_DIR)
RESULT_DIR = 'Results_fewshot/MFP_self_open/'
model_performance += load_results(RESULT_DIR)
RESULT_DIR = 'Results_fewshot/BSP_self_close/'
model_performance += load_results(RESULT_DIR)
RESULT_DIR = 'Results_fewshot/BSP_self_open/'
model_performance += load_results(RESULT_DIR)

result_df = []
for expr_result in model_performance:
    result = calculate_accuracy(expr_result)
    expr_df = pd.DataFrame(columns=['model', 'problem', 'level', 'Average accuracy', 'Failure', 'difference'])
    model_name = result['model']
    difference = result['difference']
    problem_name = result['problem']
    accuracy = result['accuracy']
    failed = result['failed']
    l = len(accuracy)
    expr_df['model'] = [model_name] * l
    expr_df['problem'] = [problem_name] * l
    expr_df['level'] = [i+1 for i in range(10 - l, 10)]
    expr_df['Average accuracy'] = accuracy
    norm_sum = (21 - l) * l / 2
    expr_df['weighted_accuracy'] = [x * (i + 1) / norm_sum for i, x in zip(range(10 - l, 10), accuracy)]
    expr_df['Failure'] = failed
    expr_df['weighted_failed'] = [x / l for i, x in enumerate(failed)]
    expr_df['difference'] = [difference] * l
    expr_df['lvl_correctness'] = result['level_correctness']
    close_models = ['gpt-4-1106-preview', 'gpt-3.5-turbo', 'claude-2', 'claude-instant-1.2', 'chat-bison@001']
    expr_df['is_close'] = [model_name in close_models] * l
    result_df.append(expr_df)
result_df = pd.concat(result_df)
result_df.to_csv('result_df_fewshot.csv')

for problem in result_df.problem.unique():
    for model in result_df.model.unique():
        tmp_df = result_df[(result_df.model == model) & (result_df.problem == problem)]
        tmp_df = tmp_df.sort_values(by=['difference', 'level'])
        tmp_df = tmp_df.pivot(index='difference', columns='level', values='Average accuracy').sort_values(by='difference', ascending=False)
        plt.figure(figsize=(10, 10))
        sns.heatmap(tmp_df, annot=True, vmin=0, vmax=1, cmap='Reds', fmt='.2f')
        plt.title(f'{model} accuracy on {problem}'.title(), fontsize=20)
        plt.xlabel('Difficulty Level', fontsize=15)
        plt.ylabel('Difficulty Difference', fontsize=15)
        plt.savefig(f'figures/{model}_{problem}_accuracy.png', dpi=500)