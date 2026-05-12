import pandas as pd
from  get_category_reason import get_category_and_reason


def process_csv(input_file, output_file):
    df = pd.read_csv(input_file)

    if 'ID' not in df.columns or 'Step Action' not in df.columns:
        raise ValueError("CSV must contain 'ID' and 'Step Action' columns")

    # Load existing output if exists
    try:
        existing_df = pd.read_csv(output_file)
        processed_ids = set(existing_df['ID'])
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=['ID', 'Step Action', 'Category', 'Reason'])
        processed_ids = set()

    for _, row in df.iterrows():
        test_id = row['ID']

        if test_id in processed_ids:
            continue  # ✅ Skip already processed

        step_action = row['Step Action']
        
        result = get_category_and_reason(step_action)
        category = result["category"]
        reason = result["reason"]
        #print("category: "+category+", reason: "+reason)

        new_row = pd.DataFrame([{
            'ID': test_id,
            'Step Action': step_action,
            'Category': category,
            'Reason': reason
        }])

        existing_df = pd.concat([existing_df, new_row], ignore_index=True)

        # ✅ Save progress
        existing_df.to_csv(output_file, index=False)

        print(f"Processed Test Case ID into category : {test_id} → {category}")


# ✅ Usage
#input_file = "output.csv"
#output_file = "output_with_category.csv"

#process_csv(input_file, output_file)