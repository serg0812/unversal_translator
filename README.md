# unversal_translator
This is the first version of tranlsator. 

Modules:
gpt4web.py - actual module which runs the translation, use generate_response 
function to do so, you can change the translation model here

pdf_to_image_from_array.py - converts pdf file into number of images page based, 
you can zoom in here if you want to, just set zoom up, default (1) is 72

process_image_from_array.py does the job, it handles images, special prompts are 
here 
as well

streamlit_play.py is the main file to run
streamlit_play1.py is the copy of the main file, you can experiment here instead 
of creating another branch

