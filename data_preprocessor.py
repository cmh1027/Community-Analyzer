import torch
import os, json
from utility import constant
from utility.constant import BertToken
from tqdm import tqdm

if __name__ == "__main__":
    articles_noexcess = []
    actual_lengths = []
    website_idxs = []
    max_len = -1
    tokenized = json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/bert_tokenized_ind.json"), 'r'))
    ########## Preprocessing ##########
    for data in tqdm(tokenized, desc="Measuring maximum size..."):
        for article in tqdm(data["content"], desc=data["name"] + " : Measuring maximum size..."):
            if max_len < len(article) and len(article) <= constant.SENTENCE_MAXLEN:
                max_len = len(article)
    website_idx = 0
    for data in tqdm(tokenized, "Removing length-excess sentences..."):
        articles = data["content"]
        articles_removed_excess = []
        for article in tqdm(articles, desc=data["name"] + " : Removing length-excess sentences..."):
            if(len(article) <= constant.SENTENCE_MAXLEN):
                articles_removed_excess.append(article)
        articles = articles_removed_excess
        article_count = len(articles)
        website_idxs.extend([website_idx] * article_count)
        for idx, article in tqdm(enumerate(articles), desc=data["name"] + " : Adding PAD tokens..."):
            article = articles[idx]
            actual_lengths.append(len(article))
            articles[idx][len(article):max_len] = [BertToken.PAD_TOKEN_IND] * (max_len - len(article))
        articles_noexcess.append(torch.tensor(articles))
    articles_noexcess = torch.cat(articles_noexcess[:], dim=0)
    website_idxs = torch.tensor(website_idxs)
    actual_lengths = torch.tensor(actual_lengths)
    torch.save(articles_noexcess, os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/articles_noexcess"))
    torch.save(website_idxs, os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/website_idxs"))
    torch.save(actual_lengths, os.path.join(os.path.abspath(os.path.dirname(__file__)), "data/actual_lengths"))