import re

special_chars = r',;:!<>()[]&?=+\"\'./\\'   

def ngram_finding(text, ngrams_dict):
    
    #Create a list of all the ngrams of the text with lenght 1 to 7
    ngrams_list, words = ngrams_funct(text)
    
    # Create a dictionary with ngrams as keys and the relative counter as value
    ngrams_dict = counter(ngrams_list, ngrams_dict)
    return ngrams_dict, words, ngrams_list

#create all the n-grams of lenght 1 to 7 from a given text 
def ngrams_funct(text): 
    count = 0
    ngrams = [] 

    # Split the sentence into words
    words = text.split()
    count += len(words)
    for length in range(1, 8):
        for i in range(len(words) - length + 1):
            ngram = tuple(words[i:i+length])
            ngrams.append(ngram)
    return ngrams, count

#counter of expression in all documents 
def counter(ngrams, ngrams_dict):   
    for ngram in ngrams:
        # Increment count for the current list in the dictionary
        ngrams_dict[ngram]['counter'] += 1
    return ngrams_dict