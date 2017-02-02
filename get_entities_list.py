from pycorenlp import StanfordCoreNLP
import json
import validator

parking_label_dict = {}

def get_entities(text):
    nlp = StanfordCoreNLP('http://localhost:9000')
    entitites_list = {}
    distance = False
    
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize, ssplit, truecase, pos, lemma, ner, regexner, entitymentions', #'tokenize,ssplit,pos,depparse,parse',
        'truecase.overwriteText': 'true',
        #'pos.model': '/Users/pradipchitrakar/Documents/TCL/NLP/py-corenlp/model/gate-EN-twitter.model',
        'regexner.mapping': '/Users/pradipchitrakar/Documents/TCL/NLP/py-corenlp/data/entity_list_arranged.txt',
        'outputFormat': 'json'
    })

    #print output

    sent_len = len(output['sentences'])


    for i in range(0, sent_len):
        token_len = len(output['sentences'][i]['tokens'])

        for j in range(0, token_len):
            k = 1
            orginialText = output['sentences'][i]['tokens'][j]['originalText']
            entity = get_matching_labels(output['sentences'][i]['tokens'][j]['ner'])

            if(entity != 'O'):
                if(entity == 'Distance_Unit'):
                    distance = True
                
                entitites_list[orginialText] = entity

    if(distance):
        for key,value in entitites_list.items():
            if value == 'Amount':
                entitites_list[key] = 'Distance_Number'
    return entitites_list

def get_ground_truth(text_raw, text_out):
    words_raw = text_raw.split()
    words_out = text_out.split()

    word_index = 0
    gnd_list = {}

    for word_out in words_out:
        if (word_out != '0'):
            gnd_list[words_raw[word_index]] = word_out

        word_index += 1

    return gnd_list


def get_entities_from_file():
    f_raw = open('data/trainRaw.txt', 'r')
    f_out = open('data/trainOut.txt', 'r')
    
    k = 1

    entities_labels = set([])
    gnd_labels = set([])

    for line_raw in f_raw:
        line_out = f_out.readline()

        entitites_list = get_entities(line_raw)
        entities_labels.update(entitites_list.values())

        gnd_list = get_ground_truth(line_raw, line_out)
        gnd_labels.update(gnd_list.values())

        check_line_for_match(entitites_list, gnd_list)

        k += 1

    f_raw.close()
    f_out.close()

def get_entities_from_json_file():
    k = 1
    
    entities_labels = set([])
    gnd_labels = set([])

    with open('data/parking_test.json') as data_file:    
        json_data = json.load(data_file)

    for entry in json_data:
        gnd_list = {}
        line_raw = entry["ground_truth"]["query"]

        entitites_list = get_entities(line_raw.encode('ascii','ignore').strip())
        entities_labels.update(entitites_list.values())

        for entity in entry["ground_truth"]["entities"]:
            for entityWord in entity["literal"].encode('ascii','ignore').split():
                gnd_list[entityWord.strip()] = entity["key"].encode('ascii','ignore').strip()
                #print (entityWord + ' : ' + entity["key"].encode('ascii','ignore'))

        gnd_labels.update(gnd_list.values())
        
        k += 1

        if k == 700:
            break
        
        check_line_for_match(entitites_list, gnd_list)


def get_entities_from_txt():
    text = "i need to find a place that i can park all day until 5 pm"

    entitites_list = get_entities(text)

    for key, value in entitites_list.iteritems():
        print(key + " : " + value)

def get_matching_labels(label):
    label = label.title()
    switch_label = {
        'Set'          : 'O',
        'Ordinal'      : 'Location',
        'Person'       : 'Location',
        'Misc'         : 'Location',
        'Organization' : 'Location',
        'Money'        : 'Amount',
        'Number'       : 'Amount',
        'Time'         : 'Calendarx',
        'Date'         : 'Calendarx'
    }

    return switch_label.get(label, label)

def check_line_for_match(entities_list, gnd_list):
    all_keys = set([])
    all_keys.update(gnd_list.keys())
    all_keys.update(entities_list.keys())

    for key in all_keys:
        gnd_value = gnd_list.get(key, 'O')
        entity_value = entities_list.get(key, 'O')
        main_value = gnd_value

        if gnd_value == 'O':
            main_value = entity_value

        if(main_value not in parking_label_dict.keys()):
            obj_label = validator.Validator(main_value)
        else:
            obj_label = parking_label_dict[main_value]

        if gnd_value == 'O':
            obj_label.FN = obj_label.FN + 1
        else:
            if gnd_value == entity_value:
                obj_label.TP = obj_label.TP + 1
            else:
                obj_label.FP = obj_label.FP + 1

        parking_label_dict[main_value] = obj_label



if __name__ == '__main__':
    #get_entities_from_file()
    get_entities_from_json_file()

    print('Precision        Recall  ')
    print ('------------------------------------------------------------')
    for key, obj in parking_label_dict.items():
        precision = (obj.TP/float(obj.TP + obj.FP) )* 100
        recall = (obj.TP/float(obj.TP + obj.FN)) * 100
        print('{0:.2f}           {1:.2f}'.format(precision, recall) + '        ' + key)
    
    #get_entities_from_txt()
    #print(get_matching_labels('PERSON'))
    