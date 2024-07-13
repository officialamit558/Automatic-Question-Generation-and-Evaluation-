from .answer_evaluation import evaluate_answer

# Weightage assignment
weight_keywords = 0.4
weight_synonyms = 0.3
weight_intent = 0.3

# Scoring algorithm
def calculate_score(matched_keywords, completion_score, intent_score):
    return (weight_keywords * matched_keywords) + (weight_synonyms * completion_score) + (weight_intent * intent_score)

# Final_score = calculate_score(matched_keywords, completion_score, intent_score)


