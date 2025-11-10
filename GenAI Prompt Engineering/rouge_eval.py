from rouge_score import rouge_scorer
import os

# -----------------------------------------------------------------------------------------------------------
# Evaluates the generated reponse given (finds the path the txt file is in to open)
# uses ROUGE evaluation scoring. There are 3 aspects that are evaluated shown below 
#
# ROUGE-N: Precision through overlap of reference and response.
# Quantifies overlap of N-grams (contiguous sequences of N items - typically words or characters) 
# between the system-generated summary and the reference summary. Provides sight on precision and recall of
# the system's output by considering the matching N-gram sequences. 
#
# ROUGE-L: Looks into COMMON synonyms to for accuracy (doesn't have to be word for word).
# Calculates "Longest Common Subsequence" (LCS) between the system and reference summaries. Measures max
# sequences of words (doesn't have to be continguous) that appear in both summaries. More flexibile
# similarity measure and helps capture shared information beyond strict word-for-word matches. 
# 
# NOTE: ROUGE 2 is uncommon, it is best to use GPT eval and BLEU for this
# ROUGE-S: Paraphrasing flexibility wording measurement.
# Skip-bigram (pair of words ina sentence that allows for gaps or words in between) focus. This identifies the 
# skip-bigram overlap between the system and reference, enabling the assessment of sentence-level structure 
# similarity. Paraphrasing relationships between sentences and provide insights into the system's ability to convey
# information with flexibile word ordering
# 
# Reference to be used is the actual privacy policy. The generated responses (system) will be then compared!
# ------------------------------------------------------------------------------------------------------------

# initialize scorer, specifies the scores I want to use
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# loop through each policy to examine and score
for file in os.listdir("privacy_policies"):
    # get the policy
    file_path = os.path.join("privacy_policies", file_path)
    #policy_name = 
    with open(file_path, "r", encoding="utf-8") as f: 
        reference = f.read()

    # get the reference summary (the LLM summary from the prompting)

    # write the output into another folder



