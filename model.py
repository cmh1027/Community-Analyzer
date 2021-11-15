from inspect import trace
import torch
from torch import nn, optim
import json, os
from utility import constant
from utility.constant import BertToken
from tqdm import trange
import argparse
from kobert.pytorch_kobert import get_pytorch_kobert_model
from kobert.utils import get_tokenizer
import gluonnlp as nlp
import matplotlib.pyplot as plt
from konlpy.tag import Okt 

def generate_square_subsequent_mask(sz: int):
    return torch.triu(torch.full((sz, sz), float('-inf')), diagonal=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str)
    parser.add_argument('--words', type=str)
    parser.add_argument('--website', type=str)
    args = parser.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if args.mode == "train":
        hidden_vector = torch.load('model/d2v.w2v_format').to(device)
        hidden_vector = torch.cat(hidden_vector.split(1)[:], dim=2).squeeze()
        articles = torch.load(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/articles_noexcess")).to(device)
        actual_lengths = torch.load(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/actual_lengths")).to(device)
        website_idxs = torch.load(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/website_idxs")).to(device)
        num_websites = len(articles)
        decoder_layer = nn.TransformerDecoderLayer(d_model=constant.EMBED_SIZE, nhead=1)
        transformer_decoder = nn.TransformerDecoder(decoder_layer, num_layers=6)
        embedding_layer = nn.Embedding(constant.BERT_VOCAB_SIZE, constant.EMBED_SIZE)
        output_linear_layer = nn.Linear(constant.EMBED_SIZE, constant.BERT_VOCAB_SIZE)
        torch.nn.init.kaiming_uniform_(decoder_layer.linear1.weight)
        torch.nn.init.kaiming_uniform_(decoder_layer.linear2.weight)
        torch.nn.init.kaiming_uniform_(embedding_layer.weight)
        torch.nn.init.kaiming_uniform_(output_linear_layer.weight)
        optimizer = optim.Adam(list(transformer_decoder.parameters())
                                + list(embedding_layer.parameters()) + list(output_linear_layer.parameters()))
        loss_weights = torch.ones(constant.BERT_VOCAB_SIZE)
        loss_weights[BertToken.PAD_TOKEN_IND] = 0.0
        losses = []
        for epoch in trange(constant.DECODER_EPOCH, desc="training..."):
            # (len, batch, embed_size)
            batchidx = torch.randint(len(articles), (constant.BATCH_SIZE,))
            length = actual_lengths[batchidx]
            hidden = hidden_vector[website_idxs[batchidx]].unsqueeze(0)
            inputs = articles[batchidx]
            label = torch.cat((inputs[:, 1:], torch.tensor([BertToken.PAD_TOKEN_IND]*constant.BATCH_SIZE).view(-1, 1)), dim=1)
            label[torch.arange(len(label)), length-1] = BertToken.END_TOKEN_IND
            b, s = inputs.shape
            sequence_mask = generate_square_subsequent_mask(constant.SENTENCE_MAXLEN)
            padding_mask = torch.zeros(b, s)
            for i, l in enumerate(length):
                padding_mask[i][l:] = 1
            tgt = inputs
            tgt = embedding_layer(tgt)
            tgt = tgt.transpose(0, 1)
            output = transformer_decoder(
                tgt=tgt, 
                memory=hidden, 
                tgt_mask = sequence_mask,
                tgt_key_padding_mask = padding_mask)
            output = output_linear_layer(output)
            output = torch.softmax(output, dim=-1)
            output = output.view(-1, output.shape[-1])
            label = label.view(-1)
            criterion = nn.CrossEntropyLoss(weight=loss_weights)
            loss = criterion(output, label)
            losses.append(loss.item())
            # if epoch % 1 == 0:
            #     print("Loss : %.3f", loss.item())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        plt.plot(range(len(losses)), losses)
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.savefig('Loss.png')
        torch.save(transformer_decoder, os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/transformer_decoder"))
        torch.save(embedding_layer, os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/embedding_layer"))
        torch.save(output_linear_layer, os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/output_linear_layer"))
    else:
        if args.words is None:
            parser.error('Starting words(sentence) is required for the evaluation')
        if args.website is None:
            parser.error('Website index is required for the evaluation')
        hidden_vector = torch.load('model/d2v.w2v_format')
        n, p, d = hidden_vector.shape
        hidden_vector = (hidden_vector.view(n, -1) * constant.WEIGHT[:, None]).view(n, p, d)
        hidden_vector = torch.cat(hidden_vector.split(1)[:], dim=-1).squeeze()
        index = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/idx2name.json"), 'r'))
        print("Language Generation in " + index[args.website] + " Style")
        okt = Okt()
        bertmodel, vocab = get_pytorch_kobert_model()
        tokenizer = get_tokenizer()
        tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
        tokens = tok(okt.normalize(args.words))
        inputs = torch.tensor(list(map(lambda s: vocab[s], tokens)))
        length = len(inputs)
        hidden = hidden_vector[int(args.website)].unsqueeze(0).unsqueeze(1)
        transformer_decoder = torch.load(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/transformer_decoder"))
        embedding_layer = torch.load(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/embedding_layer"))
        output_linear_layer = torch.load(os.path.join(os.path.abspath(os.path.dirname(__file__)), "model/output_linear_layer"))
        while length < constant.SENTENCE_MAXLEN:
            tgt = inputs
            tgt = embedding_layer(tgt)
            tgt = tgt.unsqueeze(0)
            tgt = tgt.transpose(0, 1)
            output = transformer_decoder(
                tgt=tgt, 
                memory=hidden
            )
            output_embed = output_linear_layer(output)
            output_embed = torch.softmax(output_embed / constant.SOFTMAX_TEMPERATURE , dim=-1)
            output_embed = output_embed[-1,:,:] # the last timestep
            prob, indices = output_embed.topk(constant.RANDOM_CHOICE, dim=-1)
            prob[indices == BertToken.UNK_TOKEN_IND] = 0
            pred_token = indices.squeeze(0)[torch.multinomial(prob, 1).squeeze(0)]
            if pred_token == BertToken.END_TOKEN_IND:
                break
            inputs = torch.cat((inputs, pred_token), dim=-1)
            length += 1
        for ind in inputs:
            word = vocab.to_tokens(ind.item())
            if word[0] == constant.BERT_UNDERLINE:
                print(" ", end="")
                word = word[1:]
            print(word, end="")