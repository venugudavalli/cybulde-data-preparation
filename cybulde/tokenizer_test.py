from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("./trained_tokenizer")

print(tokenizer)

text = ["Hello, world!"]

encoded = tokenizer.batch_encode_plus(text)

print(encoded)
