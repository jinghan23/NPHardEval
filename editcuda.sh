#!/bin/bash

export CUDA_HOME="/ssddata/local/cuda-12.1"
export PATH="${CUDA_HOME}/bin:${PATH}"
export LD_LIBRARY_PATH="${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}"