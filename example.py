from pycorenlp import StanfordCoreNLP

if __name__ == '__main__':
    f_raw = open('data/trainRaw.txt', 'r')
    nlp = StanfordCoreNLP('http://localhost:9000')
    text = (
        'where is the nearest open lot')
    
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
            print(output['sentences'][i]['entitymentions'][j]['text'] + ' : ' + output['sentences'][i]['entitymentions'][j]['ner'])

    #print(output)
    #print(output['sentences'][0]['parse'])
    #print(output['sentences'][0]['tokens'][7]['ner'])
    #print(output['sentences'][0]['entitymentions'][2]['text'] + ' : ' + output['sentences'][0]['entitymentions'][2]['ner'])
    #print(len(output['sentences'][0]['tokens']))
    
    #output = nlp.tokensregex(text, pattern='/buddhism|last/', filter=False)
    #print(output)
    
    #output = nlp.semgrex(text, pattern='{tag: VBD}', filter=False)
    #print(output)
