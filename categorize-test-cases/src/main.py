from extract_columns  import extract_id_steps
from categorize_test_cases import process_csv
import streamlit as st
import os





#input_folder = r"C:\Users\Kuldeep.Tiwari\OneDrive - Arrivia\Desktop\Documents\Testing\MemberHubTestCases\Phase 2\MemberCreation"
interim_file_path = "intermediate_file.csv"
output_file = "output_with_category.csv"

def process(input_folder):
    # Step 1 - read exported excel sheets, extract ID and Steps columns and save to a new csv fil
    
    st.write("Extracting ID and Steps from Excel files...")
    extract_id_steps(input_folder, interim_file_path) 

    output_file_path = os.path.join(input_folder, output_file)
    # Step 2 - Read the csv file, iterate through each 
    st.write("Categorizing each test case using LLM.  Don't worry, this will take some time... ")
    st.write("The output file will be saved at: ")
    st.write(output_file_path)
    st.write("Don't open this file as it is being written to, wait for the success message before opening it.")
    process_csv(interim_file_path, output_file_path)
    os.remove(interim_file_path)
      # a. call model to get category and reason for category 
      # b. update the output csv 
    st.write("Finished processing all test cases. Output saved to "+output_file)

#process(input_folder) 