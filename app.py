import streamlit as st

# Set page configuration
st.set_page_config(page_title="Automated Grader", layout="centered")

# Heading
st.title("📝 Automated Answer Grader")
st.subheader("Upload the student's paper and the answer key to calculate the score.")

# Layout with two columns
col1, col2 = st.columns(2)

# Supported file types
# Supported file types
image_types = ['png', 'jpg', 'jpeg']
all_types = ['pdf', 'docx', 'txt'] + image_types

with col1:
    answer_sheet = st.file_uploader("Upload Answer Sheet", type=all_types)
    # Preview logic for Answer Key
    if answer_sheet is not None:
        if answer_sheet.name.split('.')[-1].lower() in image_types:
            st.image(answer_sheet, caption="Answer Sheet Preview", use_container_width=True)
        else:
            st.info(f"File '{answer_sheet.name}' uploaded (Preview not available for this format).")

with col2:
    answer_key = st.file_uploader("Upload Answer Key", type=all_types)
    # Preview logic for Answer Key
    if answer_key is not None:
        if answer_key.name.split('.')[-1].lower() in image_types:
            st.image(answer_key, caption="Answer Key Preview", use_container_width=True)
        else:
            st.info(f"File '{answer_key.name}' uploaded (Preview not available for this format).")

# Button to trigger grading
if st.button("Calculate Score"):
    if answer_sheet and answer_key:
        print(answer_key)
        # --- PLACEHOLDER FOR GRADING LOGIC ---
        # You would implement your text extraction and comparison logic here.
        
        score = 85  # Placeholder value
        description = "The student demonstrated a strong understanding of the core concepts, though there were minor errors in the final section."
        
        # --- Output Section ---
        st.divider()
        st.header("Results")
        
        # Metric display for score
        st.metric(label="Final Score", value=f"{score}%")
        
        # Description display
        st.subheader("Performance Summary")
        st.write(description)
        
    else:
        st.warning("Please upload both files to proceed.")