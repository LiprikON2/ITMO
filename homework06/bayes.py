from db import News, session, engine
from math import log
from nltk.tokenize import RegexpTokenizer
from pprint import pprint as pp
from operator import itemgetter

class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.labels = []
        self.classified_words = [] # list of word_info dicts

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. 
        X - news title
        y - news label (upvoted, downvoted, maybe'ed)
        """
        # List unique classes (labels)
        self.labels = list(set(y))
        
        tokenizer = RegexpTokenizer(r'\w+')
        
        words = []
        sanitized_titles = []
        for title in X:
            # Remove punctuation and lowercase words
            sanitized_title = list(map(str.lower, tokenizer.tokenize(title)))
            
            sanitized_titles.append(' '.join(sanitized_title))
            words.extend(sanitized_title)
        
        unique_words = list(set(words))
        for word in unique_words:
            word_info = {
                'word': word,
                'occur_in_class': [], # list of dicts
                'total_count': 0,
                'prob_in_class': [], # list of dicts
            }
            
            # Dynamically count word occurences in classes (labels)
            for label in self.labels:
                count = 0
                for title_index, title in enumerate(sanitized_titles):
                    if y[title_index] == label:
                        count += title.count(word)
                        
                # print(word, 'occurs in', label, count, 'times')
                word_info['occur_in_class'].append({
                    f'{label}': count,
                })
            
            # Count occurences in ALL classes (labels)
            total_count = 0
            for occur in word_info['occur_in_class']:
                total_count += list(occur.values())[0]
            word_info['total_count'] = total_count
                
            # Dynamically count word probabilities for appearing in classes (labels)
            for label in self.labels:
                for occur in word_info['occur_in_class']:
                    if list(occur.keys())[0] == label:
                        occur_in_class = occur[f'{label}']
                
                # Formula: https://i.imgur.com/oaym6LY.png 
                prob = log((occur_in_class + self.alpha)/(total_count + self.alpha * len(unique_words)))
                
                # print(word, 'has', prob, 'probabilty of appearing in', label)
                word_info['prob_in_class'].append({
                    f'{label}': prob
                })
            
            self.classified_words.append(word_info)
        # pp(self.classified_words)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        tokenizer = RegexpTokenizer(r'\w+')
        
        predictions = []
        for title in X:
            # Remove punctuation and lowercase words
            sanitized_title = list(map(str.lower, tokenizer.tokenize(title)))
            
            
            prob_sums = []
            for label in self.labels:
                prob_sum = log(1 / len(labels))
                
                for word in sanitized_title:
                    word_info = list(filter(lambda word_info: word_info['word'] == word, self.classified_words))
                    
                    # print(word, 'is in', word_info, 'dict')
                    if word_info:
                        word_info = word_info[0]
                        for prob in word_info['prob_in_class']:
                            if list(prob.keys())[0] == label:
                                prob_in_class = prob[f'{label}']
                                prob_sum += prob_in_class
                prob_sums.append((label, prob_sum))
            
            
            # ref: https://stackoverflow.com/questions/13145368/find-the-maximum-value-in-a-list-of-tuples-in-python
            prediction = (title, max(prob_sums,key=itemgetter(1))[0], max(prob_sums,key=itemgetter(1))[1])
            predictions.append(prediction)
        return predictions
            
        
            
    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        success = 0
        fail = 0
        for i in range(len(X_test)):
            print(X_test[i][1])
            if X_test[i][1] == y_test[i]:
                success += 1
            else:
                fail += 1
        total = success + fail
        accuracy = success / total
        print(accuracy)
        # X_test
    
if __name__ == '__main__':
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    titles = [row.title for row in rows]
    labels = [row.label for row in rows]
    bayers = NaiveBayesClassifier()
    bayers.fit(titles[:700], labels[:700])
    predictions = bayers.predict(titles[701:])
    bayers.score(predictions, labels[701:])