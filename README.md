# NPHardEval: Benchmarking Reasoning Ability of Large Language Models via Complexity Classes


## Overview
NPHardEval serves as a comprehensive benchmark for assessing the reasoning abilities of large language models (LLMs) through the lens of computational complexity classes. This repository contains datasets, data generation scripts, and experimental procedures designed to evaluate LLMs in various reasoning tasks.
<div align="center">
    <img src="NP-hard.jpg" alt="Questions of different complexity classes" style="width:80%">
</div>


## Environment setup
### Install environments
```bash
conda create --name llm_reason python=3.10
conda activate llm_reason
git clone https://github.com/casmlab/NPHardEval.git
pip install -r requirements.txt
```

### Set-up API keys
Please set up your API keys in `secrets.txt`. **Please don't directly upload your keys to any public repository.**

## Data Structure
**Directory:** `Data`

The `Data` directory houses the datasets utilized in our study, categorized into `Fewshot` and `Zeroshot` datasets, corresponding to their respective experimental setups.

**Structure:**
```bash
$ tree -d Data 
Data
├── Fewshot
│   └── FewshotExample
└── Zeroshot
    ├── BSP
    ├── EDP
    ├── GCP
    ├── GCP_Decision
    ├── KSP
    ├── MFP
    ├── MSP
    ├── SPP
    ├── TSP
    └── TSP_Decision
```

### Data
The data used is under `data` directory. You can find the zeroshot/fewshot under the corresponding directory. They are the data used in our report.


## Data Generation
**Directory:** `generate`

In the generate directory, scripts for creating data instances tailored to different reasoning tasks are provided. These scripts are essential for generating both zero-shot and few-shot test questions. Additionally, we include utility functions for validating generated instances, ensuring quality and relevance.

**Special Mention for Fewshot Data Generation:**
Under `generate/answer_generate`, we provide templates for creating few-shot examples, offering guidance for extending this methodology to additional reasoning tasks.

**Structure:**
```bash
$ tree generate
generate
├── answer_generate
│   ├── answer_p_mfp.py
│   └── answer_p_spp.py
├── check_spp_mfp_instance.py
├── generate_cmp_GCP_D.py
├── generate_cmp_KSP.py
├── generate_cmp_TSP_D.py
├── generate_hard_GCP.py
├── generate_hard_MSP.py
├── generate_hard_TSP.py
├── generate_p_BSP.py
├── generate_p_EDP.py
├── generate_p_MFP.py
└── generate_p_SPP.py
```


## Experiments
To successfully replicate the experiments detailed in this repository, the following prerequisites must be met:

1. **Access to Large Language Model (LLM) APIs**: Essential for interfacing with the LLMs under evaluation.
2. **Datasets**: Located in the `Data` directory, these datasets are vital for conducting both zero-shot and few-shot experiments.
3. **Script Utilization**: Scripts located in the `run` directory are designed to facilitate the experimental process. This repository is meticulously organized to support distinct experimental approaches for zero-shot and few-shot scenarios.

### Execution Script
**Directory:** `run` \
**File**: `run.sh`

This script is your primary tool for experiment execution. It is meticulously crafted to provide a seamless and efficient experimental workflow. Detailed instructions within `run.sh` guide users through each step of the process, ensuring a smooth and error-free execution.

```bash
$ tree run    
run
├── models.py
├── prompts.py
├── run.sh
├── run_fewshot
│   ├── run_p_BSP.py
│   ├── run_p_EDP.py
│   ├── run_p_MFP.py
│   └── utils.py
└── run_zeroshot
    ├── run_cmp_GCP_D.py
    ├── run_cmp_KSP.py
    ├── run_cmp_TSP_D.py
    ├── run_hard_GCP.py
    ├── run_hard_MSP.py
    ├── run_hard_TSP.py
    ├── run_p_BSP.py
    ├── run_p_EDP.py
    ├── run_p_MFP.py
    ├── run_p_MFP_more.py
    ├── run_p_SPP.py
    ├── run_p_SPP_more.py
    └── utils.py

```


### Answer Verification
**Directory**: `check`

Contained within this directory are utility functions crucial for verifying answers provided by the LLMs. These functions are automatically invoked during experiments executed via `run.sh`. As the experiment progresses, these utilities rigorously evaluate the responses from LLMs and compile the outcomes in the `Results` directory. This automated process ensures a comprehensive and objective assessment of the LLM's performance.


## Analysis
**Directory:** `summary`

This directory primarily focuses on the visualization and analysis of data related to the performance of Large Language Models (LLMs). It includes two key components:

**Jupyter Notebooks**: `result_complexities.ipynb` analyzes the accuracy rates of LLMs across various question complexity classes, while `result_problems.ipynb` examines specific problem instances and their solutions as processed by LLMs.

**Source Code** (`src` sub-directory): This sub-directory contains Python scripts dedicated to the visualization and analysis of ablation studies and research questions (RQs). The scripts, named as `visualize_ablation*.py` and `visualize_rq*.py`, provide detailed insights into different aspects of LLM performance and characteristics.

Overall, the summary directory serves as a comprehensive hub for assessing and understanding the efficacy of Large Language Models in handling questions of varying complexities and types.