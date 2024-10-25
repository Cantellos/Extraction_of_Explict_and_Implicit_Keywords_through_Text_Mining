import random

#PRECISION
def precision(re, metric):
    #Select randomly 200 RE from the list
    if len(re) < 200:
        raise ValueError("The vector contains less than {} elements.".format(200))
    r = random.sample(re,200)
    print("\nRandom sample of 200 RE to evaluate Precision for the metric "+metric)
    print(r)
    #Select by your judgement the true RE
    true=int(input("\nInsert the number of true RE: "))
    return true/200

#RECALL
def recall(re_dict):
    #Find 200 RE in 10 paragraphs of four corpus files that are 2-17-25-180
    positive= [ "The blue crane","national bird of South Africa",
                "large scale photo","realistic ballpoint duplications",
                "phenolic resin", "sexual preference disorders",
                "snapshots of friends","blue pens","largest sport hub in the city",
                "football clubs","Premier League",
                "HMS Bellerophon was in serious trouble", "fires broke out simultaneously",
                "200 casualties","suffered significant damage",
                "solitary bee nests are called aggregations","record shop named Helvete",
                "black metal","Switzerland did not join the EU customs",
                "Navy and USMC Naval Aviators","demonstration pilots and narrator"," three Hulk",

                "Ann Schmeltz Bowers","Noyce Foundation","who ran a time",
                "few months","on 5 September 2010","during Operation Blue Star", "The female record",
                "Wall Street Journal","The red military uniform","British soldiers", "red coats",
                "Olympic champion in London","increased legal immigration","comprehensive immigration reform",
                "Rajiv Gandhi","President Zail",
                "President of the Congress","Indian Parliament",
                "corrupt politics","Holloway apparently",
                
                "Hindu faith","Christian faith","Muslim faith","dharma connection","permanent dharma",
                "Christian theology","missionary preacher","divine love nectar",
                "hand cymbals dancing","mridangas dancing","subspace weapon","high yield detonations",
                "Tera Cochranes mechanism","film costume designer","Palatino digitisations",
                "Parlament digitisations","Praxis digitisations","assured destruction strategy","mutually assured destruction",
                "death penalty debate","biotechnology debate","southern part of the State","case insensitive operations","smash case operations",
                "sieve of Eratosthenes","prime number sieves","object oriented programming","air chaffer innovation",
                "chaff and straw accumulation","international associates","regional offices","coaxial cables","dielectric material",
                "dielectric losses","relative permittivity","inhomogeneous dielectric","non-circular conductor",
                "epistemic argument","mobile phone", "Richard Attenborough",
                
                "BBC Radio","independent political party","Socialist Workers Party","Role in Parliament",
                "zinnias native to North America","annuals shrubs sub shrubs","opposite stalkless leaves",
                "white chartreuse flowers","orange red purple flowers","Steve loyal to Winslows","genuine family member",
                "opera complete recordings","compact disc technology","Farfisa organ replacement","independence and division",
                "coaching links improvement","Lowell ' s next book","Civil War hero","Cold War", "nuclear war", "1993 recording"]
    
    positive = [tuple(expression.split()) for expression in positive]
    print(positive)

    set_positive = set(positive)
    set_relative_expression = set(re_dict)
    
    common_expressions = set_positive & set_relative_expression
    
    true = len(common_expressions)
    r = true/200
    return r

#F-METRIC
def Fmetric(p,r):
    f_metric = 2*p*r/(p+r)
    return f_metric