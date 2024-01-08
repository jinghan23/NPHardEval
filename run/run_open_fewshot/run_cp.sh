#!/bin/bash

# CUDA_VISIBLE_DEVICES=2 python run_p_BSP.py meta-llama/Llama-2-13b-hf --prompt_question_type BSP --difficulty_level 0
# CUDA_VISIBLE_DEVICES=3 python run_p_BSP.py \
#     "/GPUFS/yt_ust_junxianh_1/jhzhang/compression_theory/Cache/models--mistralai--Mistral-7B-v0.1/snapshots/26bca36bde8333b5d7f72e9ed20ccda6a618af24" \
#     --prompt_question_type BSP \
#     --difficulty_level 0
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

# models=(
#     # "/GPUFS/yt_ust_junxianh_1/jhzhang/compression_theory/Cache/models--deepseek-ai--deepseek-llm-7b-base/snapshots/7683fea62db869066ddaff6a41d032262c490d4f/"
#     "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--01-ai--Yi-6B/snapshots/173ac4317fc620b4f82c8fb23280b04a86b95dda/"
#     "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--meta-llama--Llama-2-7b-hf/snapshots/6fdf2e60f86ff2481f2241aaee459f85b5b0bbb9/"
#     "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--meta-llama--Llama-2-13b-hf/snapshots/99afe33d7eaa87c7fc6ea2594a0e4e7e588ee0a4/"
#     "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--Qwen--Qwen-7B/snapshots/6b28d4086be837085ff7768fb7e0253919aa6591/"
#     "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--Qwen--Qwen-14B/snapshots/11054a3048cee0621dc321ac82240dbf4c4d3da9/"
#     # "mistralai/Mistral-7B-v0.1"
#     "/GPUFS/yt_ust_junxianh_1/jhzhang/compression_theory/Cache/models--EleutherAI--llemma_7b/snapshots/acc26c54609e9f18bf31fc5d58b5b533239e0430/"
# )

models=(
    # "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--codellama--CodeLlama-7b-hf/snapshots/bc5283229e2fe411552f55c71657e97edf79066c/"
    # "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--codellama--CodeLlama-13b-hf/snapshots/a49a368460ad22e43dfffb97a1e1b826a6418d3b/"
    # "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--tiiuae--falcon-7b/snapshots/898df1396f35e447d5fe44e0a3ccaaaa69f30d36/"
    # "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--huggyllama--llama-7b/snapshots/8416d3fefb0cb3ff5775a7b13c1692d10ff1aa16/"
    # "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--huggyllama--llama-13b/snapshots/bf57045473f207bb1de1ed035ace226f4d9f9bba/"
    # "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--mosaicml--mpt-7b/snapshots/00f72b21dd089db80c7fb50cb606996751500f6d/"
    # "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--tiiuae--falcon-40b/snapshots/4a70170c215b36a3cce4b4253f6d0612bb7d4146/"
    # "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--huggyllama--llama-30b/snapshots/2b1edcdb3c7ced7bce6c1aa75c94545777c3118b/"
    # "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--mosaicml--mpt-30b/snapshots/e1fe10a573e7e9688a648131933a76d9bdca2c47/"
    # "/GPUFS/yt_ust_junxianh_1/jhzhang/compression_theory/Cache/models--EleutherAI--llemma_34b/snapshots/08634a81f7bc7343f94d1c82fae461ad9b03e233/"
    # "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--01-ai--Yi-34B/snapshots/f9d78c565fc739f3f3d1c393a6d31473b053c657/"
    "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--Qwen--Qwen-72B/snapshots/3c79efc9f83b018708e29835043610befcc42713/"
    "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--huggyllama--llama-65b/snapshots/49707c5313d34d1c5a846e29cf2a2a650c22c8ee/"
    "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--meta-llama--Llama-2-70b-hf/snapshots/cc8aa03a000ff08b4d5c5b39673321a2a396c396/"
    "/GPUFS/yt_ust_junxianh_1/.cache/huggingface/hub/models--deepseek-ai--deepseek-llm-67b-base/snapshots/c3f813a1121c95488a20132d3a4da89f4a46452f/"
)

for model in "${models[@]}"; do
    CUDA_VISIBLE_DEVICES=6,7 python run_p_BSP.py $model --prompt_question_type BSP --difficulty_level 0
done

# models=(
#     "deepseek-ai/deepseek-llm-7b-base"
#     "01-ai/Yi-6B"
#     "meta-llama/Llama-2-7b-hf"
#     "meta-llama/Llama-2-13b-hf"
#     "Qwen/Qwen-7B"
#     "Qwen/Qwen-14B"
#     "mistralai/Mistral-7B-v0.1"
#     "EleutherAI/llemma_7b"
# )

# for model in "${models[@]}"; do
#     CUDA_VISIBLE_DEVICES=3 python run_p_EDP.py $model --prompt_question_type EDP --difficulty_level 0
# done