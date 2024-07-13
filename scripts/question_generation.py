from rake_nltk import Rake
from nltk.corpus import wordnet
from transformers import pipeline
import random

# Initialize Rake for keyword extraction
rake = Rake()

def generate_distractors(word):
    """
    Function to generate distractors (incorrect answer choices) using WordNet synonyms.
    """
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            # Avoid terms with underscores and limit to one-word synonyms
            if '_' not in lemma.name() and lemma.name().lower() != word.lower():
                synonyms.add(lemma.name())
    return list(synonyms)[:3]

def generate_mcqs(content, num_mcqs):
    """
    Generate Multiple Choice Questions (MCQs) based on keywords extracted from content.
    Each MCQ has one correct answer and three distractors.
    """
    rake.extract_keywords_from_text(content)
    keywords = rake.get_ranked_phrases()[:num_mcqs]

    mcqs = []
    for idx, keyword in enumerate(keywords):
        distractors = generate_distractors(keyword)
        if len(distractors) < 3:
            continue  # Skip if not enough distractors are found
        options = distractors + [keyword]
        random.shuffle(options)
        question = f"{idx+1}. What is {keyword}?"
        mcqs.append({'question': question, 'options': options})
    
    return mcqs

def generate_short_description_questions(content, num_short_desc):
    """
    Generate short description questions based on text summarization of content.
    Each question starts with "Describe".
    """
    summarizer = pipeline("summarization")
    summaries = summarizer(content, max_length=150, min_length=30, num_return_sequences=num_short_desc, do_sample=False)

    short_questions = []
    for idx, summary in enumerate(summaries):
        question = f"{idx+1}. Describe {summary['summary_text']}"
        short_questions.append(question)
    
    return short_questions

def generate_long_description_questions(content, num_long_desc):
    """
    Generate long description questions based on text summarization of content.
    Each question starts with "Explain".
    """
    summarizer = pipeline("summarization")
    summaries = summarizer(content, max_length=300, min_length=100, num_return_sequences=num_long_desc, do_sample=False)

    long_questions = []
    for idx, summary in enumerate(summaries):
        question = f"{idx+1}. Explain {summary['summary_text']} in detail."
        long_questions.append(question)
    
    return long_questions

def generate_case_study_questions(content, num_case_studies):
    """
    Generate case study questions based on text chunks.
    Each question asks for analysis of the case study scenario.
    """
    summarizer = pipeline("summarization")
    chunks = split_content(content)
    case_studies = summarizer(chunks, max_length=500, min_length=200, num_return_sequences=num_case_studies, do_sample=False)

    case_study_questions = []
    for idx, case in enumerate(case_studies):
        question = f"{idx+1}. Analyze the following case study: {case['summary_text']}. What are the key points?"
        case_study_questions.append(question)
    
    return case_study_questions

def split_content(content, max_chunk_size=1024):
    """
    Split content into chunks based on maximum chunk size.
    """
    sentences = content.split('.')
    current_chunk = ""
    chunks = []
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += sentence + '.'
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '.'
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def generate_questions(content, num_mcqs, num_short_desc, num_long_desc, num_case_studies):
    """
    Generate various types of questions based on user input.
    """
    mcqs = generate_mcqs(content, num_mcqs)
    short_desc_questions = generate_short_description_questions(content, num_short_desc)
    long_desc_questions = generate_long_description_questions(content, num_long_desc)
    case_study_questions = generate_case_study_questions(content, num_case_studies)

    return mcqs, short_desc_questions, long_desc_questions, case_study_questions
