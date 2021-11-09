import torch
import torch.nn as nn
import json, os
import constant

hidden_vector = torch.load('model/d2v_merged.model.w2v_format')
index = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/idx2name.json"), 'r'))

decoder_layer = nn.TransformerDecoderLayer(d_model=100, nhead=5)
transformer_decoder = nn.TransformerDecoder(decoder_layer, num_layers=6)
memory = torch.rand(1, 32, constant.VECSIZE) # (len, batch, embed_size)
tgt = torch.rand(20, 32, constant.VECSIZE)
out = transformer_decoder(tgt, memory)