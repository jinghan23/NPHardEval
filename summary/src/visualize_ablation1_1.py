"""Aggregate the results of ablation study and visualize them."""
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
from visualize_utils import *

rcParams['figure.dpi'] = 500
rcParams['savefig.dpi'] = 500
rcParams['figure.figsize'] = 15, 16
rcParams['font.family'] = 'Arial'
# rcParams['font.size'] = 18
rcParams['axes.labelsize'] = 18
rcParams['axes.titlesize'] = 18
# rcParams['xtick.labelsize'] = 18
# rcParams['ytick.labelsize'] = 18
rcParams['legend.fontsize'] = 18
rcParams['figure.titlesize'] = 18
rcParams['markers.fillstyle'] = 'none'

a = mpimg.imread("figures/ablation/bspResults_accuracy.png")
b = mpimg.imread("figures/ablation/edpResults_accuracy.png")

plt.subplot(1, 2, 1)
plt.imshow(a)
plt.title('a. Sorted Array Search (SAS)', loc='left', fontsize=20)
plt.axis('off')
plt.subplot(1, 2, 2)
plt.imshow(b)
plt.title('b. Edit Distance Problem (EDP)', loc='left', fontsize=20)
plt.axis('off')
plt.tight_layout()
plt.savefig('figures/ablation/ablation_1.png', bbox_inches='tight')


zero_shot_df = pd.read_csv('results.csv')
few_shot_df = pd.read_csv('result_fewshot.csv')
few_shot_df['model'] = few_shot_df['model'].map(model_mapper)


study_problem = ['bspResults', 'edpResults']
a = zero_shot_df[zero_shot_df.problem.isin(study_problem)].groupby(
    ['model', 'problem'],
    as_index=False
).agg({
    'weighted_accuracy': 'sum',
    'weighted_failed': 'sum'
})

b = few_shot_df.groupby(
    ['model', 'problem', 'difference'],
    as_index=False
).agg({
    'weighted_accuracy': 'sum',
    'weighted_failed': 'sum'

})
for value in ['weighted_accuracy', 'weighted_failed']:
    for problem in study_problem:
        c = a[a.problem == problem].copy()
        d = b[b.problem == problem].copy()
        c.model = c.model.apply(lambda x: x.title())
        d.model = d.model.apply(lambda x: x.title())
        c['difference'] = 'Zeroshot'
        c = c.pivot(columns='model', index='difference', values=value)
        d = d.pivot(columns='model', index='difference', values=value).sort_index()
        d.index = [f'Fewshot ({i})' for i in d.index]
        all_df = pd.concat([c, d]).dropna(axis=1)
        # format the values
        all_df = all_df.map(lambda x: f'{x:.4f}')
        all_df.to_csv(f'data/ablation/{value}_{problem}_zero_few_cmp.csv')
