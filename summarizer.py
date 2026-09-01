from transformers import pipeline

# load model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):

    if len(text) > 1000:
        text = text[:1000]

    summary = summarizer(text, max_length=120, min_length=40, do_sample=False)

    return summary[0]['summary_text']