import requests

query = "Cos'è l'entropia"
url = "https://api.qwant.com/api/search/web?count=10&offset=0&q={key}&t=web&uiv=4&locale=it_It"
#results = qwant.items("site:wikipedia.org " + query, count=5)

ignored_words = ["il", "lo", "la", "i", "gli", "le", "che", "anche", "ma", "un", "uno", "una"]
ignored_websites = ["youtube.com"]

MIN_POINTS = 1

def consistent(item, query):
    """
    Consistent Algorithm
    @author Colasuonno
    Sign web desc with % value 
    0 - infinity 
    / / / / /  
    WEIGHTS:
    position: 0.2 / pos
    query words in item desc: times (excluded multiple times)
    articoli/preposizioni/congiunzioni: 0 (NONE)
    EXCLUDING:
    every desc wich does not contain all words (articoli/preposizioni/congiunzioni excluded)


    NOTE:
    EVERY WORD (VERBS INCLUDED) WILL BE FOUND WITH THE LAST WORD REPLACED WITH e,o,a,i


    RESULT:
    Once we have the result, the desc is parsed with the correct phrase
    
    """

def closest_space_in_sentence(sentence, query_words):
    ws = sentence.split(" ")
    min_space = 100000 # Just high number

    for i in range(len(ws)):
        for j in range(len(ws)-1, -1, -1):
            if str(ws[i]).lower() in query_words and str(ws[j]).lower() in query_words:
                pos = abs( i - j )
                if pos < min_space:
                    min_space = pos
    return min_space
  #  print("MIN SPACE FOR " + sentence)
  #  print("QUERY: " + str(query_words))
  #  print("MIN: " + str(min_space))
            
def analyze(query_words, valid, alternatives):
    current_min_space = 10000 # high number
    current_min_sentence = -1
    for s in valid.split("."):
        spaces = closest_space_in_sentence(s, query_words)
        if spaces < current_min_space:
            current_min_space = spaces
            current_min_sentence = s
    print("SPACES MIN: " + str(current_min_space))
    print("RESULT:")
    print(current_min_sentence)


def answer(query):
    results = requests.get(str(url).replace("{key}", query).replace(" ", "%20"),headers={'User-agent': 'Mozilla/5.0'})
    r = results.json()
    current_valid_points = -1
    current_valid = None
    alternatives = []
    items = r["data"]["result"]["items"]
    for i in items:
        flag = False
        for iw in ignored_websites:
            if iw in i["url"]:
                print("IGNORING WEBSITE " + iw + " URL: " + i["url"])
                flag = True
        if not flag:
            print("ANALYZE " + i["url"])
      #      print(i["desc"])
            points, cws = contains_all(query, i["desc"])
            if points <= MIN_POINTS:
                if current_valid_points != -1 and current_valid_points == points:
                    alternatives.append(i)
                if current_valid_points == -1 or current_valid_points > points:
                    current_valid_points = points
                    current_valid = i
                
    if current_valid_points != -1:
        print("VALID POINTS " + str(current_valid_points))
        print(current_valid["desc"])
    for a in alternatives:
        print("\n")
        print("ALTERNATIVE SAME POINTS")
        print(a["desc"])
        print("\n")
                
    return cws, current_valid, alternatives



def contains_all(query, desc):
    query = str(query).lower()
    ws = query.split(" ")
    for a in ws:
        if a == "" or a in ignored_words:
            ws.remove(a)
    
    # print("QUERY " + str(ws))
   # print("\n")
    cws = ws.copy()
    for wq in cws:
        for d in desc.split(" "):
     #       print(d + " - "+ wq + " " + str(( str(wq).lower() == str(d).lower())) )
            if str(wq).lower() == str(d).lower():
      #          print(ws)
      #          print(wq)
                if wq in ws:
                    ws.remove(wq)
    return len(ws), cws
            
cws, current_valid, alternatives = answer(query)
analyze(cws, current_valid["desc"], alternatives)
