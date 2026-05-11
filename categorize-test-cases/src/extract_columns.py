import os
import pandas as pd

def read_excel_files(folder_path):
    combined_data = []

    # Iterate through all Excel files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_excel(file_path)

            # Ensure required columns exist
            if 'ID' not in df.columns or 'Step Action' not in df.columns:
                print(f"Skipping file (missing columns): {file_name}")
                continue

            current_id = None
            current_steps = []

            for _, row in df.iterrows():
                id_val = row['ID']
                step = row['Step Action']

                # Detect empty row (separator)
                if pd.isna(id_val) and pd.isna(step):
                    if current_id is not None:
                        combined_data.append({
                            "ID": current_id,
                            "Step Action": " | ".join(current_steps)
                        })
                    current_id = None
                    current_steps = []
                    continue

                # New ID encountered
                if pd.notna(id_val):
                    if current_id is not None:
                        combined_data.append({
                            "ID": current_id,
                            "Step Action": " | ".join(current_steps)
                        })
                    current_id = id_val
                    current_steps = []

                # Add step if present
                if pd.notna(step):
                    current_steps.append(str(step).strip())

            # Handle last group in file
            if current_id is not None and current_steps:
                combined_data.append({
                    "ID": current_id,
                    "Step Action": " | ".join(current_steps)
                })

    return combined_data


def write_to_csv(data, output_file):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Output written to {output_file}")


# ✅ Usage


def extract_id_steps(input_folder_path, output_file_path): 
    combined_data = read_excel_files(input_folder_path)
    write_to_csv(combined_data, output_file_path)