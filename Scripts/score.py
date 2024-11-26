from rouge_score import rouge_scorer
import sys


def calculate_self_rouge_score(original_text, generated_summary):
    # Initialize the ROUGE scorer with the desired metrics
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    # Calculate the ROUGE score by comparing the generated summary to the original text
    scores = scorer.score(original_text, generated_summary)
    
    return scores


def main():

        # Example usage
    original_text =  sys.argv[1]
    generated_summary = sys.argv[2]

    # Calculate ROUGE scores
    self_rouge_scores = calculate_self_rouge_score(original_text, generated_summary)
    print(self_rouge_scores)


if __name__ == '__main__':
    main()