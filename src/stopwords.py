def stopwords_funct(ngrams_dict):
    #create dictionary with each stopwords and the releative bigGramNeigh value
    stopwords_count = biGramNeig(ngrams_dict)

    for stopword, value in stopwords_count.items():
        
        #calculate number of syllabes of that stopword
        syllabes = count_syllabes(stopword)
        if syllabes == 0: #special case: only numbers words
            syllabes = 1
        #calculate neigSyl    
        neigSyl = stopwords_count[stopword] / syllabes
        
        #create new dicitonary with the neigSyl value for each stop words in order to plot them
        stopwords_count[stopword]=neigSyl
        
    #sorting the dicitonary based on neigSyl value in descending order
    stopwords_count = dict(sorted(stopwords_count.items(), key=lambda item: item[1], reverse=True))
        
    # Extract values and create ranks
    values = list(stopwords_count.values())
    
    """
    Slides formula approach (HAS SOME PROBLEMS)
    
    #Calculate the absolute difference |f(r + Δk) - f(r)|
    delta_k = 4 #try also with k= from 5 to 10
    b = find_max_difference(values, delta_k)
    """
    
    b = find_b_easy(values)
    
    # Create an empty list to store the top B keys
    stopwords_list = []
    
    # Iterate over the sorted dictionary and append the first B keys to the list
    for key in stopwords_count:
        stopwords_list.append(key)
        if len(stopwords_list)==b:
            break
    return stopwords_list, b

def biGramNeig(ngrams_dict):
    stopwords_list={}
    stopwords_count={}
    #create the dictionary with a list of stopwords for each middle word
    for ngram, value in ngrams_dict.items():
        if len(ngram) == 3:
            #take the middle word of every 3-gram
            stopwords_list.setdefault(ngram[1], [])
            #append the previous and the next words to the list relating to the middle word
            stopwords_list[ngram[1]].extend([ngram[0],ngram[2]])
            
    #create the dictionary with the counter of different words in the stopwords list of each middle word
    for stopword in stopwords_list:
        #delete duplicates from every list in order to count them
        stopwords_list[stopword]=list(set(stopwords_list[stopword]))
        #counting unique items in the stopwords list and assigning that value to the realtive word in the dictionary
        stopwords_count.setdefault(stopword, {})
        stopwords_count[stopword] = len(stopwords_list[stopword])
    return stopwords_count

def count_syllabes(ngram): # n° syllabes = n° vocals - n° 2 vocals in a row (it's good approsimation)
    vocals='aeiouyAEIOUY'
    count=0
    for i in range(len(ngram)):
                if ngram[i] in vocals:
                    count += 1
                    if i < len(ngram) - 1:
                        if  ngram[i+1] in vocals:
                            count -= 1
    return count

def count_syllabes_ngram(ngram):
    for word in ngram:
        vocals='aeiouyAEIOUY'
        count=0
        for i in range(len(word)):
                    if word[i] in vocals:
                        count += 1
                        if i < len(word) - 1:
                            if  word[i+1] in vocals:
                                count -= 1
    return count

def find_max_difference(values, delta_k):
    max_diff = -float('inf')
    b = None
    for i in range(len(values) - 1 - delta_k, -1+delta_k, -1):
        diff = abs(values[i+delta_k] - values[i])  # Calculating the absolute difference between consecutive values
        if diff >= delta_k and diff > max_diff:
            max_diff = diff
            b = i  # The index i represents the rank
    return b

def find_b_easy(values):
    i = 0 
    while i < len(values) and values[i] > i:
        i += 1
    return i
            