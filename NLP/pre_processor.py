# pre_processor.py

import os
import argparse
import json
import emoji
import nltk
import re
import sys

class Pre_processor:
    def __init__(self, top_folder, score):
        self.top_folder = top_folder
        self.score = score

    def pre_processing(self):
        '''
        Output: 
        [package name].txt: filtered comments for each app
        raw_comments_[top_folder]_[score].txt: all filtered comments in this folder
        '''
        all_comments_path = os.path.join(self.top_folder, 'raw_comments_' + self.top_folder.split(os.path.sep)[-1] + '_' + str(self.score) + '.txt')
        if os.path.exists(all_comments_path):
            os.remove(all_comments_path)

        paths = self.get_comments_paths()
        for path in paths:
            self.load_raw_comments(path)
            self.process_comments()
            path = os.path.splitext(path)[0] + '.txt'
            self.write_to_file(self.comments, path, 'w+')
            self.write_to_file(self.comments, all_comments_path, 'a+')
    
    def collect_comments_by_folder(self):
        '''
        Collect comments by folder after the comments.txt for each app is generated.
        Output:
        
        [folder].txt
        '''
        
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            if dirpath.split(os.path.sep)[-1] == 'Reviews':
                comments_in_folder = []
                save_path = dirpath.replace(os.path.sep + 'Reviews', '') + '.txt'
                for filename in filenames:
                    if filename.startswith('review') and filename.endswith('txt'):
                        with open(os.path.join(dirpath, filename), "r", encoding="utf8") as f_comment:
                            for line in f_comment:
                                # print(line)
                                comments_in_folder.append(line)
                if os.path.exists(save_path):
                    os.remove(save_path)
                self.write_to_file(comments_in_folder, save_path, 'a+')   

    def collect_comments_by_category(self):
        '''
        Collect comments by category after the [folder].txt is generated.
        Output:
        raw_comments_[category].txt
        ''' 
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            for filename in filenames:
                path_category_comment = os.path.join(r'Z:\RS\Comments\try', '_'.join(filename.split('_')[:-4]) + '.txt')
                with open(os.path.join(dirpath, filename), 'r', encoding='utf8') as f_folder_comment:
                    with open(path_category_comment, 'a+', encoding='utf8') as f_category_comment:
                        for line in f_folder_comment:
                            if not line in f_category_comment:
                                f_category_comment.write(line)


    def get_comments_paths(self):
        '''
        Return the paths of comments files (review_*.json)
        '''
        comments_paths = []
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            if dirpath.split(os.path.sep)[-1] == 'Reviews':
                for filename in filenames:
                    if filename.startswith('review') and filename.endswith('json'):
                        comments_paths.append(os.path.join(dirpath, filename))
        return comments_paths

    def load_raw_comments(self, comments_path):
        '''
        Load comments into self.comments
        '''
        with open(comments_path, "r", encoding="utf8") as f_comments:
            try:
                self.comments = json.load(f_comments)
            except:
                print(comments_path)
                sys.exit()
    
    def process_comments(self, stem=False, emoji_convert=False, lower=False, english=False,length=5):
        '''
        Filter the comments according to the targed scores.
        Conduct pre-process, including converting to lower cases, convert emoji to text, drop non-english words, stemming, and length filter 
        Output: pre-processed comments in self.comments
        '''
        comments = []
        for comment in self.comments['data']:
            if comment['score'] in self.score:
                if comment['text'] is not None:
                    text = comment['text']
                    if lower:
                        text = text.lower()
                    if emoji_convert:
                        text = emoji.demojize(text)
                    if english:
                        text = self.regex_filter(text)
                    if stem:
                        text = self.stem(text)
                    if len(text.split(" ")) > length:
                        comments.append(text)
        self.comments = comments

    def regex_filter(self, text):
        '''
        Drop non-english words
        '''
        new_text = []
        for word in text.split(" "):
            if re.search("^[a-zA-Z]+$", word):
                new_text.append(word)
        return " ".join(new_text)

    def stem(self, text):
        '''
        Stemming using nltk
        '''
        token_words = nltk.word_tokenize(text)
        stem_sentence=[]

        wordnet_lemmatizer = nltk.stem.WordNetLemmatizer()
        for word in token_words:
            stem_sentence.append(wordnet_lemmatizer.lemmatize(word))
            stem_sentence.append(" ")
        return "".join(stem_sentence)

    def write_to_file(self, content, path, mode):
        with open(path, mode, encoding="utf8") as out_f:
            for line in content:
                if line:
                    out_f.write(line + '\n') 
    


def main():
    # folder_path = r'Z:\RS\Testing_1'
    folder_path = sys.argv[1]
    score = [1,2]
    Pre_processor(folder_path, score).pre_processing()
    # Pre_processor(folder_path, score).collect_comments_by_category()

if __name__ == "__main__":
    main()
