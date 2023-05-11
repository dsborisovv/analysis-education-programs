import streamlit as st
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from scipy import spatial


tokenizer = BertTokenizer.from_pretrained('../configs/rubert-tiny')
model = BertModel.from_pretrained('../configs/rubert-tiny')
rubert_tiny_centroid = np.load('../app/data/centroids/rubert_tiny_centroid.npy')


def main():
    st.title("BERT Embeddings Demo")
    text = st.text_input("Enter a sentence:")
    if text:
        embeddings = get_bert_embeddings(text)
        st.write("Cosine similarity:")
        st.write(1 - spatial.distance.cosine(embeddings, rubert_tiny_centroid))


def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
    return np.array(embeddings.tolist())


if __name__ == '__main__':
    main()
