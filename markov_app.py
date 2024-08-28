import streamlit as st
from markov_chian import run_mkov

if 'text_len' not in st.session_state:
    st.session_state.text_len = 50

if 'text_n_grams' not in st.session_state:
    st.session_state.text_n_grams = 2

if 'cahr_len' not in st.session_state:
    st.session_state.cahr_len = 5

if 'char_n_grams' not in st.session_state:
    st.session_state.char_n_grams = 2
    
if 'char_iter' not in st.session_state:
    st.session_state.char_iter = 0

st.title("Let's Markovify")
st.write("This is a simple web app that uses Markov chains to generate text based on the input text you provide. It's a fun way to generate new text that sounds like it was written by you!")

st.sidebar.title("Markovify Menu")
st.sidebar.header("Settings for Markov Word Generator")

st.session_state.text_len = st.sidebar.slider("Choose the length of the generated text", 1, 100, 50, key=1)
st.session_state.text_n_grams = st.sidebar.slider("Set the n-grams level", 1, 10, 2, key=2)

st.sidebar.header("Settings for Markov Character Generator")
st.session_state.cahr_len = st.sidebar.slider("Choose the character generation length", 1, 20, 5, key=3)
st.session_state.char_n_grams = st.sidebar.slider("Set the n-grams level", 1, 10, 2, key=4)
st.session_state.char_iter = st.sidebar.slider("Number of iterations", 1, 10, 0, key=5)

file_data = st.file_uploader("Upload a text file", type=["txt"])

if file_data is not None:
    file_data = file_data.read()
    st.write("File uploaded successfully!")
    input1 = st.text_input("Enter the text to be completed", "Arduino is an open-source electronics platform based on easy-to-use hardware and software" )
    input2 = st.text_input("Enter the charcter of word to completed", "Ard" )
    if input1 and input2:
        with st.spinner("Generating text based on the input text..."):
            char, char_itr, para = run_mkov(str(file_data), st.session_state.char_n_grams, input2, st.session_state.char_iter, input1, st.session_state.text_len)
        st.write("The Generated text is:", para)
        st.write("The Generated char from input is:" , char)
        with st.expander("Show Iterations"):
            for i in char_itr:
                st.write(i)
        
        
    
    

