def add_metrics(ngrams_dict, N):
    
    for i in range(7, 1, -1):
        for ngram in ngrams_dict:
            if len(ngram) == i:
                if ngrams_dict[ngram]["scp"] == 0:
                    ngrams_dict = scp_calculation(ngrams_dict, ngram)
                if ngrams_dict[ngram]["dice"] == 0:
                    ngrams_dict = dice_calculation(ngrams_dict, ngram)
                if ngrams_dict[ngram]["phi2"] == 0:
                    ngrams_dict = phi2_calculation(ngrams_dict, ngram, N)
                
                if i > 2:
                    ngrams_dict = scp_calculation(ngrams_dict, ngram[:i-1])
                    ngrams_dict = scp_calculation(ngrams_dict, ngram[-i+1:])
                    ngrams_dict[ngram]['On-1_scp'] = max(ngrams_dict[ngram[:i-1]]['scp'], ngrams_dict[ngram[-i+1:]]['scp'])
                    ngrams_dict = dice_calculation(ngrams_dict, ngram[:i-1])
                    ngrams_dict = dice_calculation(ngrams_dict, ngram[-i+1:])
                    ngrams_dict[ngram]['On-1_dice'] = max(ngrams_dict[ngram[:i-1]]['dice'], ngrams_dict[ngram[-i+1:]]['dice'])
                    ngrams_dict = phi2_calculation(ngrams_dict, ngram[:i-1], N)
                    ngrams_dict = phi2_calculation(ngrams_dict, ngram[-i+1:], N)
                    ngrams_dict[ngram]['On-1_phi2'] = max(ngrams_dict[ngram[:i-1]]['phi2'], ngrams_dict[ngram[-i+1:]]['phi2'])
                    
    return ngrams_dict

#Filter ngrams to get Relevant Expression
def filter(ngrams_dict, stopwords):
    
    re_dict = {
        'scp': [],
        'dice': [],
        'phi2': []
    }    
    glues=['scp', 'dice', 'phi2']
    
    special_chars = r',;:!<>()[]&?=+\"./\\'  
    p = 2 #we could try also with 1 or 3
    
    for glue in glues:
        for ngram in ngrams_dict:
            if all(char not in ngram for char in special_chars):
                if ngrams_dict[ngram]['counter'] > 1 and ngram[0] not in stopwords and ngram[len(ngram)-1] not in stopwords:
                    if len(ngram) == 2:
                        if ngrams_dict[ngram][glue] >= ngrams_dict[ngram]['On+1_'+glue]:
                            re_dict[glue].append(ngram)
                    elif 2 < len(ngram) < 7:
                        if ngrams_dict[ngram][glue] >= (((ngrams_dict[ngram]['On-1_'+glue])**p)+((ngrams_dict[ngram]['On+1_'+glue])**p)/2)**(1/p):
                            re_dict[glue].append(ngram)
    return re_dict

def scp_calculation(ngrams_dict, ngram):
    n=len(ngram)
    
    ngram_freq = ngrams_dict[ngram]['counter']
    
    numerator = ngram_freq ** 2
    denominator = 0
    
    for i in range(1, n):
        prefix = ngram[:i]
        suffix = ngram[i:]
        
        prefix_freq = ngrams_dict[prefix]['counter']
        suffix_freq = ngrams_dict[suffix]['counter']
        
        denominator += (prefix_freq * suffix_freq) / (n - 1)
    
    if denominator != 0:
        scp_score = numerator / denominator
    else:
        scp_score = 0
    
    ngrams_dict[ngram]['scp'] = scp_score
    
    if n > 2:
        #I already add the value for the smaller n-grams
        if ngrams_dict[ngram]['scp'] > ngrams_dict[ngram[:n-1]]['On+1_scp']:
            ngrams_dict[ngram[:n-1]]['On+1_scp'] = ngrams_dict[ngram]['scp']
        if ngrams_dict[ngram]['scp'] > ngrams_dict[ngram[-n+1:]]['On+1_scp']:
            ngrams_dict[ngram[-n+1:]]['On+1_scp'] = ngrams_dict[ngram]['scp']
    
    return ngrams_dict

def dice_calculation(ngrams_dict, ngram):
    n=len(ngram)
  
    ngram_freq = ngrams_dict[ngram]['counter']
    
    numerator = ngram_freq * 2
    denominator = 0
    
    for i in range(1, n):
        prefix = ngram[:i]
        suffix = ngram[i:]
        
        prefix_freq = ngrams_dict[prefix]['counter']
        suffix_freq = ngrams_dict[suffix]['counter']
        
        denominator += (prefix_freq + suffix_freq) / (n - 1)
    
    if denominator != 0:
        dice_score = numerator / denominator
    else:
        dice_score = 0
    
    ngrams_dict[ngram]['dice'] = dice_score
    
    if n > 2:
        #aggiungo già il valore per gli n-grams più piccoli
        if ngrams_dict[ngram]['dice'] > ngrams_dict[ngram[:n-1]]['On+1_dice']:
            ngrams_dict[ngram[:n-1]]['On+1_dice'] = ngrams_dict[ngram]['dice']
        if ngrams_dict[ngram]['dice'] > ngrams_dict[ngram[-n+1:]]['On+1_dice']:
            ngrams_dict[ngram[-n+1:]]['On+1_dice'] = ngrams_dict[ngram]['dice']
    
    return ngrams_dict

def phi2_calculation(ngrams_dict, ngram, N):

    n=len(ngram)
    ngram_freq = ngrams_dict[ngram]['counter']

    avQ = avQ_calc(ngrams_dict, ngram, n)
    avD = avD_calc(ngrams_dict, ngram, n, N)
    
    numerator = (N * ngram_freq - avQ) ** 2
    denominator = avD
    
    if denominator != 0:
        phi2_score = numerator / denominator
    else:
        phi2_score = 0
    
    ngrams_dict[ngram]['phi2'] = phi2_score
    
    if n > 2:
        #aggiungo già il valore per gli n-grams più piccoli
        if ngrams_dict[ngram]['phi2'] > ngrams_dict[ngram[:n-1]]['On+1_phi2']:
            ngrams_dict[ngram[:n-1]]['On+1_phi2'] = ngrams_dict[ngram]['phi2']
        if ngrams_dict[ngram]['phi2'] > ngrams_dict[ngram[-n+1:]]['On+1_phi2']:
            ngrams_dict[ngram[-n+1:]]['On+1_phi2'] = ngrams_dict[ngram]['phi2']
    
    return ngrams_dict

def avQ_calc(ngrams_dict, ngram, n):
    avQ = 0
    for i in range(1, n):
        prefix = ngram[:i]
        suffix = ngram[i:]
        
        prefix_freq = ngrams_dict[prefix]['counter']
        suffix_freq = ngrams_dict[suffix]['counter']
        
        avQ += (prefix_freq * suffix_freq) / (n - 1)
    return avQ

def avD_calc(ngrams_dict, ngram, n, N):
    avD = 0
    for i in range(1, n):
        prefix = ngram[:i]
        suffix = ngram[i:]
        
        prefix_freq = ngrams_dict[prefix]['counter']
        suffix_freq = ngrams_dict[suffix]['counter']
        neg_prefix_freq = N - prefix_freq
        neg_suffix_freq = N - suffix_freq
        
        avD += (prefix_freq * suffix_freq * neg_prefix_freq * neg_suffix_freq) / (n - 1)
    return avD
