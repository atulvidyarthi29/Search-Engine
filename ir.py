import os
import re
import nltk
from pprint import pprint


class SearchEngine:
    def __init__(self, fileslocation, typ ,query):
        self.document_no = 0
        self.inverted_index = {}
        self.boolean_list = {}
        self.permuterm_index = {}
        self.create_inverted_matrix(fileslocation)
        self.create_boolean_matrix()
        self.create_permuterm_index()
        if typ == 0:
            result = self.query_not_wild(query)
            self.retrieve_list(result)
        elif typ == 3:
            result = self.boolean_list[query]
            self.retrieve_list(result)
        elif typ == 1:
            result = self.query_wild(query)
            if len(result) == 0:
                print('No Result')
            else:
                for i in result:
                    print(i, self.inverted_index[i])
        elif typ == 2:
            result = self.wild_combination(query)
            if len(result) == 0:
                print('No Result')
            else:
                for i in result:
                    try:
                        print(i, self.inverted_index[i])
                    except:
                        pass

    def retrieve_list(self,result):
        if 1 not in result:
            print("No documents found")
            return
        count = 0
        for filename in os.listdir():
            if result[count] == 1:
                print(filename)
            count += 1

    def create_inverted_matrix(self, fileslocation):
        terms = {}
        os.chdir(fileslocation)
        for filename in os.listdir():
            f = open(os.path.join(fileslocation, filename), 'r')
            s = nltk.word_tokenize(f.read().lower())
            for i in s:
                try:
                    if filename not in terms[i]:
                        terms[i].append(filename)
                except:
                    terms[i] = []
                    terms[i].append(filename)
        for key in terms.keys():
            if not (key[0] < 'a' or key[0] > 'z'):
                self.inverted_index[key] = terms[key]
        # pprint(self.inverted_index)

    def create_boolean_matrix(self):
        for key in self.inverted_index.keys():
            self.boolean_list[key] = []
            for filename in os.listdir():
                if filename in self.inverted_index[key]:
                    self.boolean_list[key].append(1)
                else:
                    self.boolean_list[key].append(0)
        self.document_no = len(os.listdir())
        # print(len(os.listdir()))
        # print(self.boolean_list)

    def create_permuterm_index(self):  # for i in list_result:
        #     print(i, self.inverted_index[i])
        for key in self.boolean_list.keys():
            rotatekey = key + '$'
            permkey = key + "$"
            length = len(permkey)
            for i in range(length):
                rotatekey = permkey[i:] + permkey[0:i]
                self.permuterm_index[rotatekey] = key
        # print(self.permuterm_index)

    def query_not_wild(self, query):
        try:
            list1 = self.boolean_list[query[0]]
        except:
            list1 = [0] * self.document_no
        try:
            list2 = self.boolean_list[query[2]]
        except:
            list2 = [0] * self.document_no
        result = []
        if query[1] == 'and':
            for i in range(len(list1)):
                result.append(list1[i] and list2[i])
        elif query[1] == 'or':
            for i in range(len(list1)):
                result.append(list1[i] or list2[i])
        elif query[1] == 'not':
            for i in range(len(list1)):
                result.append(int(not (list1[i])))
        return result

    def fetch_postinglist(self, qu):
        list_result = []
        for keys in self.permuterm_index.keys():
            if qu in keys:
                list_result.append(self.permuterm_index[keys])
        list_result = set(list_result)
        return list_result

    def query_wild(self, query):
        query = query.split('*')
        if len(query) == 1:
            try:
                print(query[0], self.inverted_index[query[0]])
            except:
                print("query not found")
            return
        result = []
        if query[0] == '' and query[1] != '':
            qu = query[1] + '$'
            list_result = self.fetch_postinglist(qu)
        elif query[0] != '' and query[1] == '':
            qu = '$' + query[0]
            list_result = self.fetch_postinglist(qu)

        else:
            qu1 = '$' + query[0]
            list_result1 = self.fetch_postinglist(qu1)
            # print(list_result1)
            qu2 = query[1] + '$'
            list_result2 = self.fetch_postinglist(qu2)
            # print(list_result2)
            list_result = list_result1.intersection(list_result2)
            print(list_result)

        return list_result

    def wild_combination(self, query):
        result = []
        if query[1] == 'and':
            if '*' in query[0]:
                qu1 = self.query_wild(query[0])
            else:
                qu1 = set([query[0]]) 
            if '*' in query[2]:
                qu2 = self.query_wild(query[2])
            else:
                qu2 = set([query[2]]) 
            # qu2 = self.query_wild(query[2])
            result = qu1.intersection(qu2)
        elif query[1] == 'or':
            if '*' in query[0]:
                qu1 = self.query_wild(query[0])
            else:
                qu1 = set([query[0]]) 
            if '*' in query[2]:
                qu2 = self.query_wild(query[2])
            else:
                qu2 = set([query[2]]) 
            result = qu1.union(qu2)
        elif query[1] == 'not':
            qu1 = self.query_wild(query[0])
            result =  set(self.boolean_list.keys()).difference(qu1)
        return result

    def print_results(self, result):
        count = 0
        for filename in os.listdir():
            if result[count] == 1:
                print(filename)
            count += 1



print("Enter a query:")
qu = input()
if '*' not in qu:
    qu =qu.lower().split()
    if len(qu) == 1:
        SearchEngine('/home/atul/Desktop/document/', 3 ,qu[0])
    else:
        SearchEngine('/home/atul/Desktop/document/', 0 ,qu)
    
    
else:
    qu = qu.lower().split()
    if len(qu) == 1:
        SearchEngine('/home/atul/Desktop/document/', 1 ,qu[0])
    else:
        SearchEngine('/home/atul/Desktop/document/', 2 ,qu)