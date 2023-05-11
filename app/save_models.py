from transformers import AutoTokenizer, AutoModel


tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
model = AutoModel.from_pretrained("cointegrated/rubert-tiny")

model.save_pretrained('../configs/rubert-tiny')
tokenizer.save_pretrained('../configs/rubert-tiny')
