import os
from collections import defaultdict
import add_spaces
import ngrams
import metrics
import stopwords
import evaluate
import keywords
from pathlib import Path

# Define the base directory (project root)
base_dir = Path(__file__).resolve().parent.parent  # Goes up two levels from src/ to space/

# Define the relative path to the data file containing the corpus of the files to be analyzed
data_file_path = base_dir / 'data' / 'corpus2mw'

# Convert the path to a string with forward slashes
input_directory_path = data_file_path.as_posix()

# Special characters
special_chars = r",;:!<>()[]&?=+\"'./\\"            

#Number of documents in the corpus
doc_counter = 0

#Size of the whole corpus
total_words=0

# Function to create the nested dictionary structure with initialized values for ngrams_dict, where to store all ngrams and relative useful attributes
def create_ngrams_dict():
    return {
        'counter': 0,         # Frequency
        'scp': 0,             # SCP metric
        'On+1_scp': 0,        # max value of SCP for n+1 grams 
        'On-1_scp': 0,        # max value of SCP for n-1 grams 
        'dice': 0,            # Dice metric
        'On+1_dice': 0,       # max value of Dice for n+1 grams 
        'On-1_dice': 0,       # max value of Dice for n-1 grams 
        'phi2': 0,            # phi2 metric
        'On+1_phi2': 0,       # max value of phi2 for n+1 grams 
        'On-1_phi2': 0,       # max value of phi2 for n-1 grams
        'doc_with_ngram': 0,  # number of document that contains the ngrams
        'freq_per_doc': {}    # frequency of the ngram for each document
    }

# Create a defaultdict that uses the custom initializer function
ngrams_dict = defaultdict(create_ngrams_dict)

# Function to create the nested dictionary structure with initialized values for keywords_dict
def create_docs_dict():
    return {
        'Tf_Idf': {},  # Tf_Idf value for each word of the document
        'size': 0,     # Size of the document
    }

#Dictionary containing the documents and the relative implicit and explicit keywords, plus some useful values
docs_dict = defaultdict(create_docs_dict)

# Function to create the nested dictionary structure with initialized values for keywords_dict
def create_keywords_dict():
    return {
        'explicit': [], # List of Explicit keywords
        'implicit': []  # List of Implicit keywords
    }

#Dictionary containing the documents and the relative implicit and explicit keywords, plus some useful values
keywords_dict = defaultdict(create_keywords_dict)

def create_word_dict():
    return {
        'corr': 0,  #Correlation value of a certain couple of words
        'ip': 0     #Intra-document proximity value of a certain couple of words
    }
    
# Dictionary to store Corr and Ip values for coples of word in order to calculate them only one time
word_dict = defaultdict(create_keywords_dict)

# Iterate over each file in the input directory
for filename in os.listdir(input_directory_path):

        input_file_path = os.path.join(input_directory_path, filename)
        processed_text=""
        
        # Read text from the input file 
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            
            original_text = input_file.read()
            #Add spaces to work more easily on the text
            processed_text = add_spaces.add_spaces_to_special_chars(original_text)

            #Create a dictionary with ngrams as key and their frequency as value + number of words analised
            ngrams_dict, words, ngrams_list = ngrams.ngram_finding(processed_text, ngrams_dict)
            
            # Assign document name to each relevant expression
            for ngram in ngrams_list:
                if filename in ngrams_dict[ngram]['freq_per_doc']:
                    ngrams_dict[ngram]['freq_per_doc'][filename] += 1
                else:
                    ngrams_dict[ngram]['freq_per_doc'][filename] = 1
                    
            #Delete duplicates
            ngrams_list = set(ngrams_list)
            
            #Each ngram appeared 1 time in this document so increase the counter 
            for ngram in ngrams_list:
                ngrams_dict[ngram]['doc_with_ngram'] += 1
        
        docs_dict[filename]['size'] = words
        #Update the value of the counter of all the words in the whole corpus
        total_words += words
        doc_counter += 1 



print("\nOriginal text:\n")
lines = original_text.splitlines()
# Stampa solo le prime 3 righe, se esistono
for i in range(min(3, len(lines))):
    print(lines[i]) 
    
print("\nProcessed text:\n")
lines = processed_text.splitlines()
# Stampa solo le prime 3 righe, se esistono
for i in range(min(3, len(lines))):
    print(lines[i]) 

del ngrams_list, ngram

print("\nNumber of documents in the corpus: "+str(doc_counter))
print("\nSize of the corpus: "+str(total_words)+" words")

#List of Stop words
stopwords_list, b = stopwords.stopwords_funct(ngrams_dict)
print("\nValue of b / Number of stopwords: "+str(b))
print("\nStopword list:")
print(stopwords_list)

#add metrics for each ngram in the dictionary
ngrams_dict = metrics.add_metrics(ngrams_dict, total_words)

#create the list of relevant expression
re_dict = metrics.filter(ngrams_dict, stopwords_list)

del stopwords_list

print("\nN° of RE found wiht SCP metric:"+str(len(re_dict["scp"])))
print("N° of RE found wiht Dice metric:"+str(len(re_dict["dice"])))
print("N° of RE found wiht phi2 metric:"+str(len(re_dict["phi2"])))

#PRECISION, RECALL AND F-METRIC
p_scp=evaluate.precision(re_dict["scp"], 'scp')
p_dice=evaluate.precision(re_dict["dice"], 'dice')
p_phi2=evaluate.precision(re_dict["phi2"], 'phi2')

print("\nPrecision values for the metrics:\n")
print("SCP: "+str(p_scp)+"\n")
print("DICE: "+str(p_dice)+"\n")
print("phi2: "+str(p_phi2)+"\n")

r_scp=evaluate.recall(re_dict["scp"])
r_dice=evaluate.recall(re_dict["dice"])
r_phi2=evaluate.recall(re_dict["phi2"])

print("\n\nRecall values for the metrics:\n")
print("SCP: "+str(r_scp)+"\n")
print("DICE: "+str(r_dice)+"\n")
print("phi2: "+str(r_phi2)+"\n")

f_scp=evaluate.Fmetric(p_scp,r_scp)
f_dice=evaluate.Fmetric(p_dice,r_dice)
f_phi2=evaluate.Fmetric(p_phi2,r_phi2)

print("\n\nF-metric values for the metrics:\n")
print("SCP: "+str(f_scp)+"\n")
print("DICE: "+str(f_dice)+"\n")
print("phi2: "+str(f_phi2)+"\n")

#Find the best metric
if(f_scp >= f_dice):
    if(f_scp >= f_phi2):
        best_metric = "scp"
    else:
        best_metric = "phi2"
elif(f_dice >= f_phi2):
    best_metric = "dice"
else:
    best_metric = "phi2"

best_metric = 'scp'
#variable best_metric contains the string with the metric we choosed to use
print("We choose the metric '"+best_metric+"' since it has the highest F-metric value.\n")

#KEYWORDS

# List of RE and single words for keywords
word_list = keywords.word_for_correlation(re_dict[best_metric])      

del re_dict

# Calculate Tf_Idf for each RE and single word of each document
for ngram in word_list:
    for document in ngrams_dict[ngram]['freq_per_doc']:
        docs_dict[document]['Tf_Idf'][ngram] = stopwords.count_syllabes_ngram(ngram) * keywords.tf_idf(ngrams_dict[ngram]['freq_per_doc'][document], docs_dict[document]['size'], doc_counter, ngrams_dict[ngram]["doc_with_ngram"])

# Find EXPLICIT keywords for each document
keywords_dict = keywords.explicit_keywords(keywords_dict, docs_dict) #TODO ONLY 10 KW
    
# Find IMPLICIT keywords
# Calculate INTER-doc. proximity (CORRELATION)
for document in keywords_dict:
    for word in word_list:
        for explicit in keywords_dict[document]['explicit']:
            if (explicit, word) not in word_dict and (word, explicit) not in word_dict and explicit != word:
                word_dict[(explicit, word)]['corr'] = keywords.correlation(explicit, word, ngrams_dict, docs_dict)

print("\nExamples couple of words with relative Correlation score:")
items = list(word_dict.items())
for i in range(min(3, len(items))):
    key, value = items[i]
    print("Words: "+str(key))
    print("Correlation: ")
    print(value['corr'])
    
print("\nExamples of the ngram dictionary with ngrams relative parameters:")
items = list(ngrams_dict.items())
for i in range(min(5, len(items))):
    key, value = items[i]
    print(f"N-gram: {key}\tValues: {value}\n")

del items
del ngrams_dict

# Calculate INTRA-doc. proximity (IP)
#TODO

print("\nExamples of Score values for a word and some document:")

# Calculate Score and assign the 5 words with higher score as Implicit keywords to documents
keywords_dict = keywords.score(keywords_dict, word_list, word_dict) 

print("\nExamples of the final dicitonary with keywords for each document:")
items = list(keywords_dict.items())
for i in range(min(3, len(items))):
    key, value = items[i]
    print("Document: "+key)
    print("Expicit Keywords: ")
    print(value['explicit'])      
    print("Implicit Keywords: ")
    print(value['implicit']) 
    
#word_dict[(explicit, word)][ip]['corr'] * math.sqrt(word_dict[(explicit, word)][ip]) for IP too    
        
