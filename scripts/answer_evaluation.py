from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from nltk.corpus import wordnet

task = "question-answering"
model_name = "distilbert-base-cased-distilled-squad"
model_revision = "626af31"
nlp = spacy.load("en_core_web_sm")
qa_model = pipeline(task, model=model_name, revision=model_revision)

def extract_keywords(text):
    doc = nlp(text)
    return [token.text for token in doc if token.is_stop != True and token.is_punct != True]

def evaluate_answer(student_answer, expert_answer):
    # Keyword Matching
    student_keywords = extract_keywords(student_answer)
    expert_keywords = extract_keywords(expert_answer)
    
    # Synonym Matching
    synonyms = set()
    for token in expert_keywords:
        for syn in wordnet.synsets(token):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())

    matched_keywords = [word for word in student_keywords if word in synonyms]
    
    # Intent Analysis
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([student_answer, expert_answer])
    intent_score = cosine_similarity(vectors[0], vectors[1])[0][0]
    
    # Completion Check
    completion_score = qa_model(question=expert_answer, context=student_answer)['score']
    
    return matched_keywords , intent_score, completion_score
