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
    model_name = expr_result['model']
    problem_name = expr_result['problem']
    correct = expr_result['correct']
    assert len(correct) == 100, f'Incorrect number of results for {model_name} on {problem_name} with {len(correct)} results'
    origin_level_correctness = [correct[i:i+10] for i in range(0, len(correct), 10)]
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
        'accuracy': level_accuracy,
        'failed': failed_expr,
        'level_correctness': origin_level_correctness
    }


#############################################################################################################
#### Load the results                                                                                    ####
#############################################################################################################

model_performance = []
RESULT_DIR = '../Results_fewshot/BSP_self_open'

for file in os.listdir(RESULT_DIR):
    if file.endswith('.json'):
        model = file.split('_')[0]
        problem = file.split('_')
        problem = "_".join(problem[1:])
        problem = problem.split('.')[0]
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
                'correct': correct
            }
            model_performance.append(performance)


#############################################################################################################
#### Aggregate the results                                                                               ####
#############################################################################################################

NUM_MODELS = 10
result_df = []
for expr_result in model_performance:
    result = calculate_accuracy(expr_result)
    expr_df = pd.DataFrame(columns=['model', 'problem', 'level', 'Average accuracy', 'Failure'])
    model_name = result['model']
    problem_name = result['problem']
    accuracy = result['accuracy']
    failed = result['failed']
    # problem_map = {
    #     'sppResults': 'p', 'mfpResults': 'p', 'bspResults': 'p',
    #     'tsp_d_Results': 'np-cmp', 'gcp_d_Results': 'np-cmp', 'kspResults': 'np-cmp',
    #     'tspResults': 'np-hard', 'gcpResults': 'np-hard', 'mspResults': 'np-hard',
    # }
    problem_map = {
        'bspResults': 'p',
    }
    expr_df['model'] = [model_name] * NUM_MODELS
    expr_df['problem'] = [problem_name] * NUM_MODELS
    expr_df['level'] = [f'Lvl {i+1}' for i in range(NUM_MODELS)]
    expr_df['Average accuracy'] = accuracy
    expr_df['weighted_accuracy'] = [x * (i+1) / 55 for i, x in enumerate(accuracy)]
    expr_df['Failure'] = failed
    expr_df['weighted_failed'] = [x / NUM_MODELS for i, x in enumerate(failed)]
    expr_df['complexity'] = [problem_map[problem_name]] * NUM_MODELS
    expr_df['lvl_correctness'] = result['level_correctness']
    close_models = ['gpt-4-1106-preview', 'gpt-3.5-turbo', 'claude-2', 'claude-instant-1.2', 'chat-bison@001']
    expr_df['is_close'] = [model_name in close_models] * NUM_MODELS
    result_df.append(expr_df)
result_df = pd.concat(result_df)

result_df.to_csv('summary/results_feew_shot_open.csv', index=False)


#############################################################################################################
#### Visualize the results                                                                               ####
#############################################################################################################

# Aggregate the results
tmp_df = result_df.groupby(['model', 'problem', 'complexity', 'is_close'], as_index=False).agg({
    'Average accuracy': 'mean',
    'weighted_accuracy': 'sum', 
    'weighted_failed': 'sum'
}).reset_index()

# Change the column name to visualize different metrics
# col_name = 'Average accuracy'
# col_name = 'weighted_accuracy'
# col_name = 'weighted_failed'

def plot_final_output(col_name, tmp_df):
    tmp_df = tmp_df.groupby(['model', 'complexity', 'is_close'], as_index=False).agg({col_name: 'mean'}).reset_index()
    mean_tmp_df = tmp_df.groupby(['complexity', 'is_close'], as_index=False).agg({col_name: 'mean'})
    mean_tmp_df['comp_order'] = mean_tmp_df['complexity'].map({'p': 1, 'np-cmp': 2, 'np-hard': 3})
    tmp_df['comp_order'] = tmp_df['complexity'].map({'p': 1, 'np-cmp': 2, 'np-hard': 3})
    tmp_df.sort_values(by=['comp_order', 'is_close'], inplace=True)
    plt.figure(figsize=(10, 6))

    # make one red palette and one blue palette
    palette = sns.color_palette("tab10", n_colors=10)
    palette = sorted(palette, key=lambda x: x[0] - x[2])
    sns.lineplot(data=tmp_df[~tmp_df['is_close']], x='complexity', y=col_name, hue='model', alpha=0.6, linestyle='--', palette=palette[:5])
    sns.lineplot(data=mean_tmp_df[~mean_tmp_df['is_close']], x='complexity', y=col_name, color='blue', marker='o', label='Open models')

    # annotate the mean value of open models
    for i, row in mean_tmp_df[~mean_tmp_df['is_close']].iterrows():
        plt.text(row['comp_order'] - 1, row[col_name] + 0.02, f'{row[col_name]:.2f}', fontsize=10, color='darkblue')
    sns.lineplot(data=tmp_df[tmp_df['is_close']], x='complexity', y=col_name, hue='model', alpha=0.6, linestyle='--', palette=palette[5:])
    sns.lineplot(data=mean_tmp_df[mean_tmp_df['is_close']], x='complexity', y=col_name, color='red', marker='o', label='Close models')

    # annotate the mean value of close models
    for i, row in mean_tmp_df[mean_tmp_df['is_close']].iterrows():
        plt.text(row['comp_order'] - 1, row[col_name] + 0.02, f'{row[col_name]:.2f}', fontsize=10, color='darkred')

    # set the title and labels
    if col_name == 'weighted_accuracy':
        plt.title(f'Weighted accuracy for different models on different complexity problems', fontsize=18)
        plt.ylabel(f'Weighted accuracy', fontsize=14)
    elif col_name == 'Average accuracy':
        plt.title(f'Average accuracy for different models on different complexity problems', fontsize=16)
        plt.ylabel(f'Average accuracy')
    else:
        plt.title(f'Weighted failure rate for different models on different complexity problems', fontsize=16)
        plt.ylabel(f'Weighted failure rate', fontsize=16)
    plt.xlabel('Complexity', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # set the legend and save the figure
    plt.tight_layout()
    if col_name == 'weighted_failed':
        plt.legend(title='Model', fontsize=12, loc='best', ncols=2)
    else:
        plt.legend(title='Model', loc='upper right', ncols=2, fontsize=12)
    plt.ylim(0, 1)
    plt.savefig(f'summary/figures/{col_name}.png', dpi=500, bbox_inches='tight')


for col_name in ['weighted_accuracy', 'weighted_failed']:
    plot_final_output(col_name, tmp_df)