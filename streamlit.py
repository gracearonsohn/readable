# Import necessary packages
import streamlit as st
import requests
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
from textstat.textstat import textstatistics
from bs4 import BeautifulSoup
import contractions
import streamlit.components.v1 as components



st.set_page_config(page_title="PS407 - Grace Aronsohn", page_icon=":computer:",layout="wide")

### Helper functions
def getText(link):
    """
    Uses the requests library to retrieve HTML from a given webpage url and the BeautifulSoup
    library to parse the HTML, returning the text content from the url as a string.
    
    Inputs: The url of the webpage to analyze, in string format.
    Outputs: The text content of the webpage, in string format.
    """
    r = requests.get(link)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    
    # Get text from <p> tags
    s = ""
    for tag in soup.body.find_all('p'):
        s += tag.text
    
    # Get text from <li> tags
    list_text = ""
    for tag in soup.body.find_all('li'):
        
        # Only include list items with length 2+
        if len(tag.text) >= 2:
            list_text += tag.text + "."
    
    return s + "." + list_text




def cleanText(str):
    """
    Cleans text to a standard format to facilitate readability calculations.
    
    Inputs: The text to clean, in string format.
    Outputs: A list of individual words in the string.
    """
    # Convert all text to lowercase
    str = str.lower()
    
    # Deal with contractions
    str = contractions.fix(str)

    # Remove all punctuation, numbers, etc.
    for i in range(0,len(str)):
        if str[i] != " " and str[i].isalpha() == False:
            str = str.replace(str[i]," ")

    # Create list of words (split by space)
    words = str.split()
            
    return words




def totalWords(text):
    """
    Calculates the total number of words in the given text.

    Inputs: The text to analyze, in string format.
    Output: An integer representing the total number of words in the given input text.
    """
    return len(text.split())




def totalSentences(text):
    """
    Calculates the total number of sentences in the given text.

    Inputs: The text to analyze, in string format.
    Output: An integer representing the total number of words in the given input text.
    """
    return len(sent_tokenize(text))



    
def totalSyllables(text):
    """
    Calculates the total number of syllables in the given text.

    Inputs: The text to analyze, in string format.
    Output: A float representing the total number of syllables in the given input text.
    """
    total = 0
    for i in cleanText(text):
        total += textstatistics().syllable_count(i)
    
    return total



    
def averageWordsPerSentence(text):
    """
    Calculates the average number of words per sentence in the given text.

    Inputs: The text to analyze, in string format.
    Output: A float representing the average number of words per sentence in the given input text.
    """
    if totalSentences(text) > 0:
        return totalWords(text)/totalSentences(text)
    else:
        return 0



    
def averageSyllablesPerWord(text):
    """
    Calculates the average number of syllables per word in the given text.

    Inputs: The text to analyze, in string format.
    Output: A float representing the average number of syllables per word in the given input text.
    """
    if totalWords(text) > 0:
        return totalSyllables(text)/totalWords(text)
    else:
        return 0




### Readability calculators
def FRE(text):
    """
    Calculates the Flesch Reading Ease score of the given text.
    
    Inputs: The text to analyze, in string format.
    Output: A float representing the FRE score of the given input text.
    """
    if text != "":
        score = 206.835 - (1.015 * averageWordsPerSentence(text)) - (84.6 * averageSyllablesPerWord(text))
    else:
        score = None
    if score < 0:
        score = 0
    elif score > 100:
        score = 100
    return score




def FK(text):
    """
    Calculates the Flesch-Kincaid score of the given text.
    
    Inputs: The text to analyze, in string format.
    Output: A float representing the F-K score of the given input text.
    """
    if text != "":
        score = (0.39 * averageWordsPerSentence(text)) + (11.8 * averageSyllablesPerWord(text)) - 15.59
    else:
        score = None
    if score < 0:
        score = 0
    return score




# ---- USE LOCAL CSS ----
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

local_css("style/style.css")

# ---- HEADER SECTION ----
with st.container():
    st.subheader("PS407 - Grace Aronsohn")
    st.title("Immortal souls, first-born children, and other things we’re signing away")
    st.write("A Comparative Study of the Terms of Service Agreements of Big Tech Companies and the Challenges for Government Regulators")
    st.write("[Read the full paper here](https://catalog.middlebury.edu/courses/view/catalog/catalog%2FMCUG/course/course%2FPSCI0407)")

# ---- CONTEXT
with st.container():
    st.write("---")
    st.header("How do we measure readability?")
    st.write("Two of the most widely used measures of readability are the Flesch Reading Ease (FRE) and Flesch-Kincaid (F-K) metrics. Both scores are calculated using the average sentence length and average number of syllables per word of a given text, varying only by the coefficients used.")
    st.write("##")
    fre_column,fk_column = st.columns(2)
    with fre_column:
        st.header("Flesch Reading Ease")
        st.write("FRE scores range from 0 to 100, with higher scores indicating greater readability, and are calculated as follows:")
        st.markdown("**206.835 - (1.015 * average words per sentence) - (84.6 * average sentences per word)**")
        #st.latex("206.835 - (1.015 * \\text{average words per sentence}) - (84.6 * \\text{average sentences per word})")
        st.write("Texts that score below 60 are considered to be unreadable to the average consumer, with a score of 60 or above being required by United States government agencies to ensure documents are readable to the public.")
    with fk_column:
        st.header("Flesch-Kincaid")
        st.write("F-K scores are associated with a grade level reading ability. The recommended score is 8.0 or less, indicating an eighth-grade reading level. F-K scores are calculated as follows:")
        st.markdown("**(0.39 * average words per sentence) + (11.8 * average syllables per word) – 15.59**")
        #st.latex("(0.39 * \\text{average words per sentence}) + (11.8 * \\text{average syllables per word}) – 15.59")
        st.write("This score is required for documents published by organizations like the Department of Education, the Food and Drug Administration, and the National Institute of Health.")




# ---- READABILITY CALCULATOR ----
with st.container():
    st.write("---")
    st.header("Try the readability calculator!")
    left_column, right_column = st.columns(2)
    with left_column:
        calculator_input = left_column.text_input("","",placeholder="Input text")
    with right_column:
        if calculator_input == "":
            st.write("##")
            st.header("Enter text to calculate readability!")
        else:
            st.write("Total number of words: " + str(totalWords(calculator_input)))
            st.write("Total number of sentences: " + str(totalSentences(calculator_input)))
            st.write("Total number of syllables: " + str(totalSyllables(calculator_input)))
            st.write("Average words per sentence: " + str(round(averageWordsPerSentence(calculator_input),2)))
            st.write("Average syllables per word: " + str(round(averageSyllablesPerWord(calculator_input),2)))
            st.write("\n")
            st.write("FRE Score: " + str(round(FRE(calculator_input),2)))
            st.write("F-K Score: " + str(round(FK(calculator_input),2)))
        


# ---- DATASET ----
with st.container():
    st.write("---")
    st.header("How readable is Big Tech?")
    st.write("Explore readability metrics of terms of service and privacy policy agreements at Amazon, Apple, Google, Meta, and Microsoft.")
    components.iframe("https://datawrapper.dwcdn.net/kopik/1/",height=500,scrolling=True)
    st.write("##")
    st.write("##")
    st.header("Google, over the years (1999 - present)")
    st.write("Google dominates over 90% of the search engine market, processing over 40,000 searches every second. However, Google's Terms of Service and Privacy Policy have only become less readable since their initial publication in 1999.")
    components.iframe("https://datawrapper.dwcdn.net/9focA/2/",height=500,scrolling=True)


# ---- CONTACT FORM ----
with st.container():
    st.write("---")
    st.header("Contact me")
    st.write("##")

    contact_form = """
    <form action="https://formsubmit.co/garonsohn@middlebury.edu" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message" required></textarea>
        <button type="submit">Send</button>
    </form>
    """

    left_column,right_column = st.columns(2)
    with left_column:
        st.write("Research by Grace Aronsohn")
        st.write("PSCI 407: Who Elected Big Tech? (Fall 2022)")
        st.write("Professor Allison Stanger | Middlebury College")
    with right_column:
        st.markdown(contact_form, unsafe_allow_html=True)
