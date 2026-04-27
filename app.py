import streamlit as st
from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv
import ocr
import evaluation
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# Set page configuration
st.set_page_config(page_title="Automated Grader", layout="centered")

# Heading
st.title("Automated Answer Grader")
st.subheader("Upload the student's paper and the answer key to calculate the score.")

# Layout with two columns
col1, col2 = st.columns(2)

# Supported file types
# image_types = ['png', 'jpg', 'jpeg']
all_types = ['pdf']

with col1:
    answer_sheet = st.file_uploader("Upload Answer Sheet", type=all_types)
    # Preview logic for Answer Key
    # if answer_sheet is not None:
    #     if answer_sheet.name.split('.')[-1].lower() in image_types:
    #         st.image(answer_sheet, caption="Answer Sheet Preview", use_container_width=True)
    #     else:
    #         st.info(f"File '{answer_sheet.name}' uploaded (Preview not available for this format).")

with col2:
    answer_key = st.file_uploader("Upload Answer Key", type=all_types)
    # Preview logic for Answer Key
    # if answer_key is not None:
    #     if answer_key.name.split('.')[-1].lower() in image_types:
    #         st.image(answer_key, caption="Answer Key Preview", use_container_width=True)
    #     else:
    #         st.info(f"File '{answer_key.name}' uploaded (Preview not available for this format).")

# Button to trigger grading
if st.button("Calculate Score"):
    if not answer_sheet and not answer_key:
        st.error("Missing Files: Please upload both the Answer Sheet and the Answer Key.")
    
    elif not answer_sheet:
        st.warning("The Answer Sheet is missing. Please upload the student's work.")
        
    elif not answer_key:
        st.warning("The Answer Key is missing. Please upload the reference key.")
    if answer_sheet and answer_key: 
        try:
            # --- PLACEHOLDER FOR GRADING LOGIC ---
            # You would implement your text extraction and comparison logic here.
            answer_sheet_bytes = answer_sheet.getvalue()
            answer_key_bytes = answer_key.getvalue()

            # contents = [
            #     "Please analyze and grade these documents.",
            #     types.Part.from_bytes(data=answer_sheet_bytes, mime_type='application/pdf'),
            #     types.Part.from_bytes(data=answer_key_bytes, mime_type='application/pdf')
            # ]
            
            contents = [
                types.Part.from_bytes(data=answer_key_bytes, mime_type='application/pdf')
            ]
            st.info("Converting answer key to json")
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                config=types.GenerateContentConfig(system_instruction=ocr.build_ocr_prompt_for_answer_key()),
                contents=contents
            )
            
            answer_key_json = json.loads(response.text.strip())
            st.info("Converted answer key to json")
            contents = [
                types.Part.from_bytes(data=answer_sheet_bytes, mime_type='application/pdf'),
            ]
            st.info("Converting answer sheet to json")
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                config=types.GenerateContentConfig(system_instruction=ocr.build_ocr_prompt_for_answer_sheet(answer_key_json)),
                contents=contents
            )
            
            answer_sheet_json = json.loads(response.text.strip())
            st.info("Converted answer sheet to json")
            st.info("Evaluating answer sheet json with answer key json")

            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                config=types.GenerateContentConfig(system_instruction="You are an expert examiner"),
                contents=evaluation.build_evaluation_prompt(answer_key_json,answer_sheet_json)
            )
            
            evaluation_json = json.loads(response.text.strip())
            st.info("Evaluated answer sheet json with answer key json")
            score = sum([e['marks_awarded']  for e in evaluation_json['evaluations']])  # Placeholder value
            description = evaluation_json['overall_feedback']
            
            # --- Output Section ---
            st.divider()
            st.header("Results")
            
            # Metric display for score
            st.metric(label="Final Score", value=f"{score}/{answer_key_json['total_marks']}")
            
            # Description display
            st.subheader("Performance Summary")
            st.write(description)
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")