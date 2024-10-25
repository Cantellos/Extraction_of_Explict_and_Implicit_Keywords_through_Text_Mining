import math

def tf_idf(freq, size, corpus, doc_freq):
    Tf_Idf = (freq / size) * math.log(corpus / doc_freq)
    return Tf_Idf

def explicit_keywords(keywords_dict, docs_dict): 
    for filename in docs_dict:
        explicit_keywords = []
        
        # Sort the nested dictionary of a certain file by the values of the Tf_Idf of each RE
        sorted_re = sorted(docs_dict[filename]['Tf_Idf'].items(), key=lambda item: item[1], reverse=True)
        
        # Keep the 15 RE with higher Tf_Idf values
        filtered_re = sorted_re[:15]
        explicit_keywords.extend([k for k, v in filtered_re])
        
        # Update the nested dictionary with the top 5 items
        keywords_dict[filename]['explicit'] = explicit_keywords
    return keywords_dict

def word_for_correlation(re_list):
    temp_list = []
    
    for re in re_list:
        first = (re[0],)
        second = (re[len(re)-1],)
        temp_list.append(first)
        temp_list.append(second)
    
    word_list = temp_list + re_list
    return list(set(word_list))
        
def correlation(a, b, ngrams_dict, docs_dict):
    cov_a = (cov(a, a, ngrams_dict, docs_dict)**0.5)
    cov_b = (cov(b, b, ngrams_dict, docs_dict)**0.5)
    if cov_a != 0 and cov_b != 0:
        corr = cov(a, b, ngrams_dict, docs_dict) / ((cov(a, a, ngrams_dict, docs_dict)**0.5)*(cov(b, b, ngrams_dict, docs_dict)**0.5))
    else: corr = 0
    return corr
   
def cov(a, b, ngrams_dict, docs_dict):
    sum = 0
    for document in ngrams_dict[a]['freq_per_doc']:
        if document in ngrams_dict[b]['freq_per_doc']:
            sum += p(a, document, ngrams_dict, docs_dict) * p(b, document, ngrams_dict, docs_dict) #approximation without p(A, .) since it's often close to zero
    cov_value = sum / (len(docs_dict) - 1)
    return cov_value

def p(ngram, document, ngrams_dict, docs_dict):
    num = ngrams_dict[ngram]['freq_per_doc'][document]
    den = docs_dict[document]['size']
    return num / den 

#TODO
def ip(ngrams_dict, re , word):
    return 0

#dist(A,B,d) - the nearest distance in number of words from occurences of A to B in d
def dist(A,B, documents):
    distances = []
    for document in documents:
            words = document.split()
            A_indices = [i for i, word in enumerate(words) if word == A]
            B_indices = [i for i, word in enumerate(words) if word == B]
            for A_index in A_indices:
                for B_index in B_indices:
                    distances.append(abs(A_index - B_index))
    return min(distances)

#farthest (A,B,d) - the farthest distance in number of words from occurences of A to B in d
def farthest(A,B, documents):
    distances = []
    for document in documents:
            words = document.split()
            A_indices = [i for i, word in enumerate(words) if word == A]
            B_indices = [i for i, word in enumerate(words) if word == B]
            for A_index in A_indices:
                for B_index in B_indices:
                    distances.append(abs(A_index - B_index))
    return max(distances)

def score(keywords_dict, word_list, word_dict):
    cont = 0
    for document in keywords_dict:
        implicit_list = []
        implicit_dict = {}
        for word in word_list:
                score = 0
                i = 1
                # calculate the score for a word (without IP for now)
                for explicit in keywords_dict[document]['explicit']:
                    if explicit != word:
                        if (explicit, word) in word_dict:
                            score += word_dict[(explicit, word)]['corr'] / i
                        else: score += word_dict[(word, explicit)]['corr'] / i
                        i += 1
                
                # Check if the score of the current word is larger than any of the scores in the list
                if len(implicit_dict) < 5 or score > min(implicit_dict[k] for k in implicit_dict):
                    # If it is, add the word to the list and keep only the 5 with higher score 
                    implicit_dict[word] = score
                    implicit_dict = dict(sorted(implicit_dict.items(), key=lambda item: float(item[1]), reverse=True))
                    if len(implicit_dict) > 5:
                        sliced_dict = list(implicit_dict.items())[:5]
                        # Convert the list of tuples back into a dictionary
                        implicit_dict = dict(sliced_dict)
        if cont < 5:
            print("\nDocument: "+document+"\nWord: "+str(word)+"\nScore: "+str(score))
        cont += 1
        
        # assign the words as Implicit keywords to documents
        for key in implicit_dict:
            implicit_list.append(key)
        keywords_dict[document]['implicit'] = implicit_list
    return keywords_dict