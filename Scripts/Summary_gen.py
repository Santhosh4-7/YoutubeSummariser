import warnings
import logging
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import sys

# Suppress warnings
warnings.filterwarnings("ignore")

# Set logging level to ERROR to suppress INFO and WARNING messages from Transformers
logging.getLogger("transformers").setLevel(logging.ERROR)

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        return str(e)

def summarize_text(text):
    summarizer = pipeline("summarization")
    max_length = 1000
    num_iters = (len(text) // max_length) + 1
    summarized_text = []

    for i in range(num_iters):
        start = i * max_length
        end = (i + 1) * max_length
        chunk = text[start:end]
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summarized_text.append(summary[0]['summary_text'])

    return " ".join(summarized_text)

if __name__ == "__main__":
    youtube_url = sys.argv[1]
    video_id = youtube_url.split("v=")[-1]
    transcript_text = get_youtube_transcript(video_id)
    summary = summarize_text(transcript_text)
    print(summary)
