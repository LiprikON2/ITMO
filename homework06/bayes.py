from db import News, session, engine
from math import log
from nltk.tokenize import RegexpTokenizer
from pprint import pprint as pp
from operator import itemgetter
import time

class NaiveBayesClassifier:

    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.labels = []
        self.classified_words = [] # list of word_info dicts
        
        self.count = {}
        
    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. 
        X - news title
        y - news label (upvoted, downvoted, maybe'ed)
        """
        t0 = time.time()
        
        
        # List unique classes (labels)
        self.labels = list(set(y))
        
        tokenizer = RegexpTokenizer(r'\w+')
        
        words = []
        sanitized_titles = []
        for index, title in enumerate(X):
            # Remove punctuation and lowercase words
            sanitized_title = list(map(str.lower, tokenizer.tokenize(title)))
            
            # Count words that occur in this class
            self.count_words_in_class(sanitized_title, y[index])
            
            sanitized_titles.append(sanitized_title)
            words.extend(sanitized_title)
        
        unique_words = list(set(words))
        for word in unique_words:
            word_info = {
                'word': word,
                'occur_in_class': [], # list of dicts
                'prob_in_class': [], # list of dicts
            }
            
            # Dynamically count word occurences in classes (labels)
            for label in self.labels:
                count = 0
                for title_index, title in enumerate(sanitized_titles):
                    if y[title_index] == label:
                        count += title.count(word)
                        
                word_info['occur_in_class'].append({
                    f'{label}': count,
                })
        
                
            # Dynamically count word probabilities for appearing in classes (labels)
            for label in self.labels:
                for occur in word_info['occur_in_class']:
                    if list(occur.keys())[0] == label:
                        occur_in_class = occur[f'{label}']
                        
                # Calculationg probability of a word appearing in class (label)
                # Formula: https://i.imgur.com/oaym6LY.png
                prob = log((occur_in_class + self.alpha)/(self.count[f'{label}'] + self.alpha * len(unique_words)))
                
                word_info['prob_in_class'].append({
                    f'{label}': prob
                })
            
            self.classified_words.append(word_info)
            
        t1 = time.time()
        total = t1-t0
        print('Fitted in %.2f' % total, 'seconds')
        
    def count_words_in_class(self, title, label):
        
        if label not in self.count:
            self.count.update({f'{label}': 0})
            
        self.count[f'{label}'] += len(title)
        

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        tokenizer = RegexpTokenizer(r'\w+')
        
        predictions = []
        for title in X:
            # Remove punctuation and lowercase words
            sanitized_title = list(map(str.lower, tokenizer.tokenize(title)))
            
            prob_sums = []
            for label in self.labels:
                prob_sum = log(1 / len(self.labels))
                
                for word in sanitized_title:
                    word_info = list(filter(lambda word_info: word_info['word'] == word, self.classified_words))
                    
                    if word_info:
                        word_info = word_info[0]
                        for prob in word_info['prob_in_class']:
                            if list(prob.keys())[0] == label:
                                prob_in_class = prob[f'{label}']
                                prob_sum += prob_in_class
                prob_sums.append((label, prob_sum))
            
            
            # ref: https://stackoverflow.com/questions/13145368/find-the-maximum-value-in-a-list-of-tuples-in-python
            prediction = {
                'title': title,
                'label': max(prob_sums,key=itemgetter(1))[0],
                'prob_sum': max(prob_sums,key=itemgetter(1))[1],
            }
            
            predictions.append(prediction)
        return predictions
            
        
            
    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        t0 = time.time()
        success = 0
        fail = 0
        predictions = self.predict(X_test)
        
        for index, _ in enumerate(predictions):
            # Compare predicted label and true label
            if predictions[index]['label'] == y_test[index]:
                success += 1
            else: 
                fail += 1
        total = success + fail
        accuracy = success / total
        

        t1 = time.time()
        total = t1-t0
        print('Predicted in %.2f' % total, 'seconds')
        print('Result accuracy: %.6f' % accuracy, f'with α={self.alpha}')

# Score on SMS Spam Collection 
if __name__ == '__main__':
    import csv
    with open("SMSSpamCollection", encoding="utf8") as f:
            data = list(csv.reader(f, delimiter="\t"))
    labels = []
    texts = []
    for pair in data:
        label, text = pair
        labels.append(label)
        texts.append(text)
    bayers = NaiveBayesClassifier()
    bayers.fit(texts[:3900], labels[:3900])
    bayers.score(texts[3900:], labels[3900:])

# Score on SMS Spam Collection by sklearn
# if __name__ == '__main__':
#     import csv
#     with open("SMSSpamCollection", encoding="utf8") as f:
#             data = list(csv.reader(f, delimiter="\t"))
#     labels = []
#     texts = []
#     for pair in data:
#         label, text = pair
#         labels.append(label)
#         texts.append(text)
#     from sklearn.naive_bayes import MultinomialNB
#     from sklearn.pipeline import Pipeline
#     from sklearn.feature_extraction.text import TfidfVectorizer

#     model = Pipeline([
#         ('vectorizer', TfidfVectorizer()),
#         ('classifier', MultinomialNB(alpha=0.05)),
#     ])

#     model.fit(texts[:3900], labels[:3900])
#     print(model.score(texts[3900:], labels[3900:]))