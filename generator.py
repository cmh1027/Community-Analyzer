import torch
import torch.nn as nn
import torch.nn.functional as function
import json, os
import constant
from kobert.pytorch_kobert import get_pytorch_kobert_model

if __name__ == "__main__":
    model, vocab  = get_pytorch_kobert_model()
    hidden_vector = torch.load('model/d2v_merged.model.w2v_format')
    index = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/idx2name.json"), 'r'))
    embed_size = constant.VECSIZE * len(constant.FORMATS)
    one_hot = []
    max_len = -1
    for d in json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/bert_tokenized_ind.json"), 'r')):
        if max_len < len(d["content"]):
            max_len = len(d["content"])
        one_hot.append({"name":d["name"], "content":list(map(lambda t:function.one_hot(torch.tensor(t)), d["content"]))})
    decoder_layer = nn.TransformerDecoderLayer(d_model=constant.BERT_VOCAB_SIZE, nhead=1)
    transformer_decoder = nn.TransformerDecoder(decoder_layer, num_layers=6)
    linear = nn.Linear(embed_size, constant.BERT_VOCAB_SIZE)
    hidden_vectors = linear(hidden_vector) # Need to be written
    
    # (len, batch, embed_size)
    memory = hidden_vectors[0].view(1, 1, -1) # sanity check

    tgt = torch.rand(max_len, constant.BATCH, constant.BERT_VOCAB_SIZE)
    out = transformer_decoder(tgt, memory)