import torch

MAXTHREAD = 4
WEBSITES = ["dcinside"]
WEBSITES_ATTIBUTES = {
    "dcinside" : {
        "rank" : 5,
        "page" : 10
    }
}
BERT_VOCAB_SIZE = 8002
PAD_TOKEN = 1
END_TOKEN = 2
FORMATS = ["bert", "okt_adjv", "okt_noun"]
DOCVEC_SIZE = 200
EMBED_SIZE = DOCVEC_SIZE*len(FORMATS)
BATCH_SIZE = 10
EPOCH = 10
WEIGHT = torch.tensor([1.0, 1.0, 1.0])
SENTENCE_MAXLEN = 50
BERT_UNDERLINE = "▁"
RANDOM_CHOICE = 10
SOFTMAX_TEMPERATURE = 1