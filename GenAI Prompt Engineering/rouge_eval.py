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

REFERENCE_FOLDER = r"privacy_policies"      # folder with actual policies
SUMMARY_FOLDER   = r"gemini_policies_4"         # folder with LLM-produced summaries
OUTPUT_PATH      = r"rouge_prompt4_results.txt"

# initialize scorer
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

results = []

# -------------------------------------------------------
# LOOP THROUGH EACH POLICY AND SCORE AGAINST MATCHING SUMMARY
# -------------------------------------------------------
for filename in os.listdir(REFERENCE_FOLDER):

    # Only process text files
    if not filename.endswith(".txt"):
        continue

    reference_path = os.path.join(REFERENCE_FOLDER, filename)
    summary_path   = os.path.join(SUMMARY_FOLDER, filename)

    # skip if the summary doesn't exist
    if not os.path.exists(summary_path):
        results.append(f"Missing LLM summary for: {filename}\n{'-'*70}\n")
        continue

    # load reference policy
    with open(reference_path, "r", encoding="utf-8") as f:
        reference_text = f.read()

    # load LLM summary
    with open(summary_path, "r", encoding="utf-8") as f:
        candidate_text = f.read()

    # compute ROUGE
    scores = scorer.score(reference_text, candidate_text)

    result_block = (
        f"FILE: {filename}\n"
        f"ROUGE-1  →  Precision: {scores['rouge1'].precision:.4f}, "
        f"Recall: {scores['rouge1'].recall:.4f}, "
        f"F1: {scores['rouge1'].fmeasure:.4f}\n"
        f"ROUGE-2  →  Precision: {scores['rouge2'].precision:.4f}, "
        f"Recall: {scores['rouge2'].recall:.4f}, "
        f"F1: {scores['rouge2'].fmeasure:.4f}\n"
        f"ROUGE-L  →  Precision: {scores['rougeL'].precision:.4f}, "
        f"Recall: {scores['rougeL'].recall:.4f}, "
        f"F1: {scores['rougeL'].fmeasure:.4f}\n"
        f"{'-'*70}\n"
    )

    results.append(result_block)

# -------------------------------------------------------
# WRITE RESULTS TO OUTPUT FILE
# -------------------------------------------------------
with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    out.writelines(results)

print("ROUGE scoring completed! Results saved to:", OUTPUT_PATH)
