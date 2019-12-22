import os
import nltk
import math
from pprint import pprint


class Ranking:

    def __init__(self, path):
        self.filelocation = path
        os.chdir(path)
        self.docs = os.listdir()
        self.documents = self.create_word_frequency()
        self.query_tokens = nltk.word_tokenize(input('Enter the query: '))
        self.query = self.query_dict()
        self.doc_mag = self.calculate_mag()
        results = self.calculate_score()
        pprint(results)

    def create_word_frequency(self):
        documents = {}
        for filename in self.docs:
            f = open(os.path.join(self.filelocation, filename), 'r')
            documents[filename] = {}
            word_tokens = nltk.word_tokenize(f.read().lower())
            for word in word_tokens:
                if (word[0] > 'a' and word[0] < 'z') or (word[0] > '0' and word[0] < '9'):
                    try:
                        documents[filename][word] += 1
                    except:
                        documents[filename][word] = 1
        return documents

    def calculate_mag(self):
        doc_mag = {}
        for filename in self.docs:
            sum1 = 0
            for subkey in self.documents[filename]:
                sum1 += (self.documents[filename][subkey]/len(self.documents[filename])) * (
                    self.documents[filename][subkey]/len(self.documents[filename]))
            doc_mag[filename] = math.sqrt(sum1)
        return doc_mag

    def query_dict(self):
        query = {}
        for word in self.query_tokens:
            if (word[0] > 'a' and word[0] < 'z') or (word[0] > '0' and word[0] < '9'):
                try:
                    query[word] += 1
                except:
                    query[word] = 1
        return query

    def calculate_score(self):
        results = []
        sum1 = 0
        for word in self.query:
            sum1 += (self.query[word]/len(self.query)) * \
                (self.query[word]/len(self.query))
        mag = math.sqrt(sum1)
        for doc in self.docs:
            sum2 = 0
            for word in self.query:
                try:
                    sum2 += self.query[word]*self.documents[doc][word] / \
                        (len(self.documents[doc]) * len(self.query))
                except:
                    pass
            score = sum2/(self.doc_mag[doc]*mag)
            results.append((doc, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results


Ranking('/home/gcoderx/Desktop/IR/document/')
