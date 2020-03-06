from db import News, session, engine
from math import log
from nltk.tokenize import RegexpTokenizer

class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.labels = []
        self.sanitized_titles = []
        self.train = [] # title + label pair

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. 
        X - news title
        y - news label (upvoted, downvoted, maybe'ed)
        """
        # List unique classes (labels)
        self.labels = list(set(y))
        # Probability of a class (label)
        self.label_probability = 1 / len(labels)
        
        tokenizer = RegexpTokenizer(r'\w+')
        
        words = []
        for title in X:
            # Remove punctuation and lowercase words
            sanitized_title = list(map(str.lower, tokenizer.tokenize(title)))
            
            self.sanitized_titles.append(' '.join(sanitized_title))
            words.extend(sanitized_title)
        
        unique_words = list(set(words))
        
        for word in unique_words[:100]:
            word_info = {
                'word': word,
                'occur_in_class': [], # list of dicts
                'total_count': 0,
                'prob_in_class': [], # list of dicts
            }
            
            # Dynamically count word occurences in classes (labels)
            for label in self.labels:
                count = 0
                for title_index, title in enumerate(self.sanitized_titles):
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
                
                prob = log((occur_in_class + self.alpha)/(total_count + self.alpha * len(unique_words)))
                
                # print(word, 'has', prob, 'probabilty of appearing in', label)
                word_info['prob_in_class'].append({
                    f'{label}': prob
                })
            
        
        # print(words)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        pass

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pass

if __name__ == '__main__':
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    titles = [row.title for row in rows]
    labels = [row.label for row in rows]
    bayers = NaiveBayesClassifier()
    bayers.fit(titles, labels)
    