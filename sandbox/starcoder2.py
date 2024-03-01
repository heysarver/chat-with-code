import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "bigcode/starcoder2-7b"
device = "cuda" # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint, torch_dtype=torch.bfloat16).to(device)

inputs = tokenizer.encode("def connect_to_elasticsearch():", return_tensors="pt").to(device)

outputs = model.generate(inputs, max_length=None, max_new_tokens=1024)
print(tokenizer.decode(outputs[0]))

print(f"Memory footprint: {model.get_memory_footprint() / 1e6:.2f} MB")
