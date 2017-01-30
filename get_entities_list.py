from pycorenlp import StanfordCoreNLP

def get_entities(text):
    nlp = StanfordCoreNLP('http://localhost:9000')
    entitites_list = {}
    
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize, ssplit, truecase, pos, lemma, ner, regexner,entitymentions', #'tokenize,ssplit,pos,depparse,parse',
        'truecase.overwriteText': 'true',
        'regexner.mapping': '/Users/pradipchitrakar/Documents/TCL/NLP/py-corenlp/data/entity_list.txt',
        'outputFormat': 'json'
    })

    sent_len = len(output['sentences'])

    for i in range(0, sent_len):
        #token_len = len(output['sentences'][i]['tokens'])
        entity_len = len(output['sentences'][i]['entitymentions'])

        #for j in range(0, token_len):
        for j in range(0, entity_len):
            k = 1
            #print(output['sentences'][i]['tokens'][j]['originalText'] + ' : ' + output['sentences'][i]['tokens'][j]['pos'])
            #print(output['sentences'][i]['entitymentions'][j]['text'] + ' : ' + output['sentences'][i]['entitymentions'][j]['ner'])
            entitites_list[output['sentences'][i]['entitymentions'][j]['text']] = output['sentences'][i]['entitymentions'][j]['ner']

    return entitites_list

if __name__ == '__main__':
    f_raw = open('data/trainRaw.txt', 'r')
    k = 1

    for line_raw in f_raw:
        entitites_list = get_entities(line_raw)
        print("..........................  " + str(k) + "  ...........................")
        for key, value in entitites_list.iteritems():
            print(key + " : " + value)

        k += 1
    