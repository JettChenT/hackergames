import hashlib
import random

from llama_cpp import Llama

# 1. Assert sha256 of the model file
model_path = "/root/qwen2.5-3b-instruct-q8_0.gguf"
expected_hash = "6dcc22694c8654b045ec40bbe350212b88893fd9010e8474bae5b19a43578ba1"

sha256_hash = hashlib.sha256()
with open(model_path, "rb") as f:
    for byte_block in iter(lambda: f.read(4096), b""):
        sha256_hash.update(byte_block)
calculated_hash = sha256_hash.hexdigest()

assert calculated_hash == expected_hash, "Model hash mismatch!"

# 2. Run the LLM with the given code
from llama_cpp import Llama

llm = Llama(
    model_path="/root/qwen2.5-3b-instruct-q8_0.gguf",
    n_ctx=1024,
    seed=random.SystemRandom().randint(0, 2**64),
)
text = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are a professional CTF player."},
        {
            "role": "user",
            "content": "Write a short article for Hackergame 2024 (中国科学技术大学 (University of Science and Technology of China) 第十一届信息安全大赛) in English. The more funny and unreal the better. About 500 words.",
        },
    ]
)["choices"][0]["message"]["content"]

# 3. Do censorship
open("/root/before.txt", "w").write(text)
open("/root/before.sha256", "w").write(hashlib.sha256(text.encode()).hexdigest())
for c in "hackergame of ustc":
    text = text.replace(c, "x")
open("/root/after.txt", "w").write(text)
