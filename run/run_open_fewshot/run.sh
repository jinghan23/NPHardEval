#!/bin/bash

# CUDA_VISIBLE_DEVICES=2 python run_p_BSP.py meta-llama/Llama-2-13b-hf --prompt_question_type BSP --difficulty_level 0
# CUDA_VISIBLE_DEVICES=3 python run_p_BSP.py 01-ai/Yi-6B --prompt_question_type BSP --difficulty_level 0
# CUDA_VISIBLE_DEVICES=1 pdython run_p_EDP.py mistral --prompt_question_type EDP --difficulty_level 0

    # 01-ai/Yi-34B\
    # meta-llama/Llama-2-7b-hf\
    # meta-llama/Llama-2-13b-hf\
    # mosaicml/mpt-7b\
    # tiiuae/falcon-7b\
    # deepseek-ai/deepseek-llm-7b-base\
    # 01-ai/Yi-6B\
    # Qwen/Qwen-7B\
    # Qwen/Qwen-14B\
    # huggyllama/llama-7b\
    # huggyllama/llama-13b\
    # mistralai/Mistral-7B-v0.1\
    # EleutherAI/llemma_7b\
    
    # codellama/CodeLlama-7b-hf\
    # codellama/CodeLlama-13b-hf\
    # 01-ai/Yi-34B\
    # huggyllama/llama-30b\
    # mosaicml/mpt-30b\
    # EleutherAI/llemma_30b\
    # tiiuae/falcon-40b\
# models=(
#     "deepseek-ai/deepseek-llm-7b-base"
#     "meta-llama/Llama-2-7b-hf"
#     "Qwen/Qwen-7B"
#     "Qwen/Qwen-14B"
#     "EleutherAI/llemma_7b"
# )

# for model in "${models[@]}"; do
#     CUDA_VISIBLE_DEVICES=3 python run_p_BSP.py $model --prompt_question_type BSP --difficulty_level 0
# done

models=(
    "deepseek-ai/deepseek-llm-7b-base"
    "01-ai/Yi-6B"
    "meta-llama/Llama-2-7b-hf"
    "meta-llama/Llama-2-13b-hf"
    "Qwen/Qwen-7B"
    "Qwen/Qwen-14B"
    "mistralai/Mistral-7B-v0.1"
    "EleutherAI/llemma_7b"
)

for model in "${models[@]}"; do
    CUDA_VISIBLE_DEVICES=3 python run_p_EDP.py $model --prompt_question_type EDP --difficulty_level 0
done