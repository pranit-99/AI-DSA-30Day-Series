
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but",
    "is", "are", "was", "were", "be", "been",
    "to", "of", "in", "on", "for", "with",
    "as", "by", "at", "from", "this", "that",
    "you", "your", "we", "our", "will", "can",
    "using", "use", "used"
}

def clean_text(text):
    text = text.lower()

    cleaned_text = ""

    for ch in text:
        if ch.isalnum() or ch.isspace():
            cleaned_text += ch

    return cleaned_text

def tokenize_text(text):
    cleaned_text = clean_text(text)

    tokens= cleaned_text.split()
    filtered_tokens = []

    for token in tokens:
        if token not in STOP_WORDS:
            filtered_tokens.append(token)

    return filtered_tokens

def get_word_frequency(text):
    tokens = tokenize_text(text)
    frequency = {}

    for token in tokens:

        if token in frequency:
            frequency[token] += 1
        else:
            frequency[token] = 1

    return frequency

def compare_resume_jd(resume_text, jd_text):

    resume_tokens = tokenize_text(resume_text)
    jd_tokens = tokenize_text(jd_text)

    resune_set = set(resume_tokens)
    jd_set = set(jd_tokens)

    matched_keywords = list(resune_set.intersection(jd_set))
    missing_keywords = list(jd_set.difference(resune_set))

    return {
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords}

def calculate_match_score(resume_text, jd_text):

    comparison_result = compare_resume_jd(resume_text, jd_text)

    matched_count = len(comparison_result["matched_keywords"])

    total_jd_keywords = len(set(tokenize_text(jd_text)))

    if total_jd_keywords == 0:
        return 0

    score = (matched_count / total_jd_keywords) * 100

    return round(score, 2)

def analyze_resume_match(resume_text, jd_text):

    comparison_result = compare_resume_jd(resume_text, jd_text)

    basic_score = calculate_match_score(resume_text, jd_text)

    weighted_score = calculate_weighted_match_score(resume_text, jd_text)
    top_missing_keywords = get_top_missing_keywords(resume_text, jd_text)

    ranked_keywords = rank_jd_keywords(jd_text)

    if weighted_score >= 75:
        suggestion = "Strong match. Resume covers the most important JD keywords."
    elif weighted_score >= 50:
        suggestion = "Medium match. Improve your resume by naturally adding: " + ", ".join(top_missing_keywords)
    else:
        suggestion = "Low match. Focus on adding these high-priority keywords: " + ", ".join(top_missing_keywords)



    return {
        "basic_match_score": basic_score,
        "weighted_match_score": weighted_score,
        "matched_keywords": comparison_result["matched_keywords"],
        "missing_keywords": comparison_result["missing_keywords"],
        "top_missing_keywords": top_missing_keywords,
        "ranked_jd_keywords": ranked_keywords,
        "suggestion": suggestion
    }
def get_important_jd_keywords(jd_text):

    jd_frequency = get_word_frequency(jd_text)

    important_keywords = []

    for word, count in jd_frequency.items():

        if count >= 1:
            important_keywords.append(word)

    return important_keywords

def rank_jd_keywords(jd_text):
    jd_frequency = get_word_frequency(jd_text)

    ranked_keywords = sorted(
        jd_frequency.items(),
        key=lambda item: item[1],
        reverse = True
    )

    return ranked_keywords

def calculate_weighted_match_score(resume_text, jd_text):
    resume_set = set(tokenize_text(resume_text))

    jd_frequency = get_word_frequency(jd_text)
    total_weight = sum(jd_frequency.values())

    matched_weight = 0

    for keyword, count in jd_frequency.items():
        if keyword in resume_set:
            matched_weight = count + 1

    score = (matched_weight / total_weight) * 100
    return round(score,2)

def get_top_missing_keywords(resume_text, jd_text, limit=5):

    resume_set = set(tokenize_text(resume_text))

    ranked_keywords = rank_jd_keywords(jd_text)

    top_missing_keywords = []

    for keyword, count in ranked_keywords:

        if keyword not in resume_set:
            top_missing_keywords.append(keyword)

        if len(top_missing_keywords) == limit:
            break

    return top_missing_keywords

resume = """
SQL AWS
"""

jd = """
Python Python Python Docker Kubernetes AWS SQL CI CD
"""

print(get_top_missing_keywords(resume, jd))
