from collections import defaultdict
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
        self.query = nltk.word_tokenize(input('Enter the query: '))
        type = int(input(
            'Enter the type of search:\n1. Raw TF\n2. Log TF\n3. Augmented TF\n4. Binary TF\n5. Okapi TF\nYour Choice: '))
        self.max1 = self.calculate_max()
        results = self.calculate_score(type)
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

    def calculate_max(self):
        max1 = 0
        for key in self.documents:
            for subkey in self.documents[key]:
                if self.documents[key][subkey] > max1:
                    max1 = self.documents[key][subkey]
        return max1

    def calculate_score(self, type):
        result = []
        for filename in self.docs:
            sum1 = 0
            for word in self.query:
                try:
                    if type == 1:
                        sum1 += self.documents[filename][word]
                    elif type == 2:
                        sum1 += 1 + math.log(self.documents[filename][word])
                    elif type == 3:
                        tf = self.documents[filename][word]
                        sum1 += 0.5 + ((0.5*tf)/self.max1)
                    elif type == 4:
                        if self.documents[filename][word] > 0:
                            sum1 += 1
                    elif type == 5:
                        tf = self.documents[filename][word]
                        sum1 += tf/(2+tf)
                except:
                    pass
            result.append((filename, sum1))
        result.sort(key=lambda x: x[1], reverse=True)
        return result


Ranking('/home/gcoderx/Desktop/IR/document/')
