import warnings
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import random
import numpy as np
import nltk
from nltk.corpus import stopwords
import string
import pke
import sys
import random

# Suppress warnings and logging messages
warnings.filterwarnings("ignore", category=FutureWarning)
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("nltk").setLevel(logging.ERROR)

# Model loading
question_model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1')
question_tokenizer = T5Tokenizer.from_pretrained('ramsrigouthamg/t5_squad_v1')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
question_model = question_model.to(device)

# Set random seed for reproducibility
def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

set_seed(42)

# Download necessary NLTK data
# nltk.download('punkt', quiet=True)
# nltk.download('brown', quiet=True)
# nltk.download('wordnet', quiet=True)

# Extract keywords using MultipartiteRank
def get_nouns_multipartite(content):
    out = []
    try:
        extractor = pke.unsupervised.MultipartiteRank()
        extractor.load_document(input=content, language='en')
        pos = {'PROPN', 'NOUN'}
        stoplist = list(string.punctuation)
        stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
        stoplist += stopwords.words('english')
        extractor.candidate_selection(pos=pos)
        extractor.candidate_weighting(alpha=1.1, threshold=0.75, method='average')

        keyphrases = extractor.get_n_best(n=15)
        for val in keyphrases:
            out.append(val[0])
    except Exception as e:
        print("Keyword extraction error:", e)
    return out[:5]

# Question generation
def get_question(context, answer, model, tokenizer):
    text = "context: {} answer: {}".format(context, answer)
    encoding = tokenizer.encode_plus(
        text, max_length=384, padding=True, truncation=True, return_tensors="pt"
    ).to(device)

    input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

    outs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        early_stopping=True,
        num_beams=5,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        max_length=72,
    )

    dec = [tokenizer.decode(ids, skip_special_tokens=True) for ids in outs]
    question = dec[0].replace("question:", "").strip()

    return question

# Main code
def main():
    summarized_text = sys.argv[1]

    # Extract important keywords
    imp_keywords = get_nouns_multipartite(summarized_text)
    
    res = {}

    # Generate questions from keywords
    for ans in imp_keywords:
        ques = get_question(summarized_text, ans, question_model, question_tokenizer)
        count = 0
        options = [ans]
        while count != 3:
            opt = random.choice(imp_keywords)
            while(opt in options):
                opt = random.choice(imp_keywords)
            options.append(opt)
            count+=1
        
        res[ques] = [ans,options]

    print(res)

if __name__ == '__main__':
    main()
