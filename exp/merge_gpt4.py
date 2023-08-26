import pandas as pd

if __name__ == "__main__":
    answered = pd.read_csv(r"data\old\500题已回答.csv")
    unanswered = pd.read_csv(r"data\questions\500_embed_sorted.csv")
    unanswered["response"] = ""

    # for each question in unanswered, find the corresponding question in answered
    # note that the question in answered may not be exactly the same as the question in unanswered
    # so if the question in answered in contained in questions answered, we assume it is the same question
    # and copy the answer over
    for index, row in unanswered.iterrows():
        for index2, row2 in answered.iterrows():
            if row["question"] in row2["Question"]:
                unanswered.at[index, "response"] = row2["Response"]
                break
    
    unanswered.to_csv(r"data\questions\500_embed_sorted_answered.csv", index=False, encoding="utf-8-sig")
