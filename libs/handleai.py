import json
import jellyfish
import unicodedata
import nltk
from libs.handledatabase import HandleDataBase
from nltk.tokenize import word_tokenize
class HandleAI():
    def __init__(self,conn,cursor):
        self.api_bot_gemeni = ''
        self.conn = conn
        self.cursor = cursor
    def normalize_text(self,text):
        return unicodedata.normalize('NFKC', text)

    def tokenize_text(self,text):
        return word_tokenize(text)

    def calculate_similarity(self,text1, text2):
        text1 = self.normalize_text(text1)
        text2 = self.normalize_text(text2)
        text1_tokens = self.tokenize_text(text1)
        text2_tokens = self.tokenize_text(text2)
        text1_string = ' '.join(text1_tokens)
        text2_string = ' '.join(text2_tokens)
        return jellyfish.jaro_winkler_similarity(text1, text2)

    def search_similar_text(self,query_text):
        # Normalize and tokenize the query text
        query_text = self.normalize_text(query_text)
        query_tokens = self.tokenize_text(query_text)

        # Get all texts from the database
        hndl = HandleDataBase(self.conn,self.cursor)
        problems = hndl.fetchOnlyProblems()
        texts = [row[0] for row in problems]

        # Find the most similar text
        best_match = None
        best_score = 0
        for text in texts:
            score = self.calculate_similarity(query_text, text)
            if score > best_score:
                best_score = score
                best_match = text

        # Return the best match
        return best_match