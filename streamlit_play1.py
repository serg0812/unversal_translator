import streamlit as st
import numpy as np
from openai import OpenAI
from gpt4web import generate_response
from text_processing import split_text_into_chunks  # Import the text processing function
from pdf_to_image_from_array import convert_pdf_to_images
from process_images_from_array import *
from docx import Document

def read_word_file(file):
    document = Document(file)
    text = []
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def main():
    st.title("File Processing and Translation")

    # Initialize session state
    if "text_input" not in st.session_state:
        st.session_state.text_input = ""
    if "translated_text" not in st.session_state:
        st.session_state.translated_text = ""
    if "pdf_images" not in st.session_state:
        st.session_state.pdf_images = None
    if "image_summary" not in st.session_state:
        st.session_state.image_summary = ""
    if "manual_text" not in st.session_state:
        st.session_state.manual_text = ""
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = None

    # Function to disable tabs
    def disable_all_tabs():
        st.session_state.processing = True

    # Function to enable all tabs
    def enable_all_tabs():
        st.session_state.processing = False
        st.session_state.active_tab = None

    # Create tabs
    tab_titles = ["PDF", "Image", "Text File", "Text Window", "MS Word"]
    tabs = st.tabs(tab_titles)

    # PDF Tab
    with tabs[0]:
        st.header("Upload PDF File")
        if st.session_state.processing and st.session_state.active_tab != "PDF":
            st.info("Processing in progress, please wait...")
        else:
            pdf_file = st.file_uploader("Upload PDF File", type=["pdf"], key="pdf_file_uploader")
            if pdf_file and pdf_file != st.session_state.get("last_uploaded_pdf"):
                st.session_state.pdf_images = convert_pdf_to_images(pdf_file)
                st.session_state.last_uploaded_pdf = pdf_file
                st.session_state.active_tab = "PDF"

            if st.session_state.pdf_images:
                has_table = st.checkbox("Does the PDF contain tables or graphs?", key="pdf_has_table")
                language = st.text_input("Enter the language to translate to", key="pdf_language")

                if st.button("Process PDF", key="pdf_process_button"):
                    disable_all_tabs()
                    if has_table:
                        text_summaries = read_images(st.session_state.pdf_images, text_prompt())
                        table_summaries = read_images(st.session_state.pdf_images, graphs_and_tables_prompt())
                        translated_texts = [generate_response(text, language) for text in text_summaries]
                        translated_tables = [generate_response(table, language) for table in table_summaries]
                        combined_summaries = "\n\n".join([f"Text: {t}\n\nTables: {g}" for t, g in zip(translated_texts, translated_tables)])
                    else:
                        text_summaries = read_images(st.session_state.pdf_images, text_prompt())
                        translated_texts = [generate_response(text, language) for text in text_summaries]
                        combined_summaries = "\n\n".join([f"Text: {t}\n\n" for t in translated_texts])

                    st.session_state.translated_text = combined_summaries
                    st.text_area("Processed Output", value=st.session_state.translated_text, height=300)
                    enable_all_tabs()

    # Image Tab
    with tabs[1]:
        st.header("Upload Image File")
        if st.session_state.processing and st.session_state.active_tab != "Image":
            st.info("Processing in progress, please wait...")
        else:
            image_file = st.file_uploader("Upload Image File", type=["jpg", "jpeg", "png"], key="image_file_uploader")
            if image_file and image_file != st.session_state.get("last_uploaded_image"):
                base64_image = encode_image_file(image_file)
                st.session_state.image_summary = base64_image
                st.session_state.last_uploaded_image = image_file
                st.session_state.active_tab = "Image"

            if st.session_state.image_summary:
                has_table = st.checkbox("Does the image contain tables or graphs?", key="image_has_table")
                language = st.text_input("Enter the language to translate to", key="image_language")

                if st.button("Process Image", key="image_process_button"):
                    disable_all_tabs()
                    if has_table:
                        text_summaries = read_images(st.session_state.image_summary, text_prompt())
                        table_summaries = read_images(st.session_state.image_summary, graphs_and_tables_prompt())
                        translated_texts = [generate_response(text, language) for text in text_summaries]
                        translated_tables = [generate_response(table, language) for table in table_summaries]
                        combined_summaries = "\n\n".join([f"Text: {t}\n\nTables: {g}" for t, g in zip(translated_texts, translated_tables)])
                    else:
                        text_summaries = read_images(st.session_state.image_summary, text_prompt())
                        translated_texts = [generate_response(text, language) for text in text_summaries]
                        combined_summaries = "\n\n".join([f"Text: {t}\n\n" for t in translated_texts])

                    st.session_state.translated_text = combined_summaries
                    st.text_area("Processed Output", value=st.session_state.translated_text, height=300)
                    enable_all_tabs()

    # Text File Tab
    with tabs[2]:
        st.header("Upload Text File")
        if st.session_state.processing and st.session_state.active_tab != "Text File":
            st.info("Processing in progress, please wait...")
        else:
            text_file = st.file_uploader("Upload Text File", type=["txt"], key="text_file_uploader")
            if text_file and text_file != st.session_state.get("last_uploaded_text_file"):
                text_array = []
                with text_file:
                    text_array.append(text_file.read().decode('utf-8'))  # Decode bytes to string
                st.session_state.text_input = text_array[0]
                st.session_state.last_uploaded_text_file = text_file
                st.session_state.active_tab = "Text File"

            if st.session_state.text_input:
                language = st.text_input("Enter the language to translate to", key="text_file_language")

                if st.button("Process Text File", key="text_file_process_button"):
                    disable_all_tabs()
                    translated_text = generate_response(st.session_state.text_input, language)
                    st.session_state.translated_text = translated_text
                    st.text_area("Processed Output", value=st.session_state.translated_text, height=300)
                    enable_all_tabs()

    # Text Window Tab
    with tabs[3]:
        st.header("Enter Text Manually")
        if st.session_state.processing and st.session_state.active_tab != "Text Window":
            st.info("Processing in progress, please wait...")
        else:
            manual_text = st.text_area("Enter your text here (up to 2000 characters)", max_chars=2000, height=300, key="manual_text_input")
            if manual_text:
                st.session_state.manual_text = manual_text
                st.session_state.active_tab = "Text Window"

            if st.session_state.manual_text:
                language = st.text_input("Enter the language to translate to", key="manual_text_language")

                if st.button("Process Manual Text", key="manual_text_process_button"):
                    disable_all_tabs()
                    text_chunks = split_text_into_chunks(st.session_state.manual_text)
                    translated_chunks = [generate_response(chunk, language) for chunk in text_chunks]
                    st.session_state.translated_text = "\n\n".join(translated_chunks)
                    st.text_area("Processed Output", value=st.session_state.translated_text, height=300)
                    enable_all_tabs()

    # MS Word Tab
    with tabs[4]:
        st.header("Upload MS Word File")
        if st.session_state.processing and st.session_state.active_tab != "MS Word":
            st.info("Processing in progress, please wait...")
        else:
            word_file = st.file_uploader("Upload Word File", type=["docx"], key="word_file_uploader")
            if word_file and word_file != st.session_state.get("last_uploaded_word_file"):
                st.session_state.text_input = read_word_file(word_file)
                st.session_state.last_uploaded_word_file = word_file
                st.session_state.active_tab = "MS Word"

            if st.session_state.text_input:
                language = st.text_input("Enter the language to translate to", key="word_file_language")

                if st.button("Process Word File", key="word_file_process_button"):
                    disable_all_tabs()
                    translated_text = generate_response(st.session_state.text_input, language)
                    st.session_state.translated_text = translated_text
                    st.text_area("Processed Output", value=st.session_state.translated_text, height=300)
                    enable_all_tabs()

if __name__ == "__main__":
    main()
