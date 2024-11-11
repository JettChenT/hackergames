#!/bin/bash

# 0. Download the model to the current folder
wget -O qwen2.5-3b-instruct-q8_0.gguf https://modelscope.cn/models/qwen/Qwen2.5-3B-Instruct-GGUF/resolve/master/qwen2.5-3b-instruct-q8_0.gguf

# 1. Build the Docker image with the Dockerfile
docker build -t llm_censor .

# 2. Run the container, mount the gguf file, and run gen.py
docker run --name llm_censor_container \
    -v "$(pwd)/qwen2.5-3b-instruct-q8_0.gguf:/root/qwen2.5-3b-instruct-q8_0.gguf" \
    llm_censor

# Copy files from the container to the current folder
docker cp llm_censor_container:/root/before.sha256 ./before.sha256
docker cp llm_censor_container:/root/before.txt ./before.txt
docker cp llm_censor_container:/root/after.txt ./after.txt

# 3. Remove the stopped container
docker rm llm_censor_container

# 4. Caculate the flag and delete uncensored file
echo "flag{llm_lm_lm_koshitantan_$(sha512sum before.txt | cut -d ' ' -f1 | cut -c1-16)}"
rm before.txt