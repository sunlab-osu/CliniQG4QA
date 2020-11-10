import numpy as np
import scispacy
import spacy
from scispacy.umls_linking import UmlsEntityLinker
import json
import random
import requests
nlp = spacy.load("en_core_sci_lg")
linker = UmlsEntityLinker()
nlp.add_pipe(linker)
tokenizer = nlp.Defaults.create_tokenizer(nlp)

#Import json data
with open('../emrQG/relations.json') as json_file:     #You can modify this line to change your input directory
    data = json.load(json_file)

#Prcoess text to add whitespace between word/letter tokens and punctuation tokens.
def process_text(text):

    temp = []
    
    token = tokenizer(text)                 #Use Spacy to do tokenization
    temp.extend(i.text for i in token)
    
    # return " ".join(Final)
    return " ".join(temp)
        
        
#Answer generator    
def generator_answer(ls, index, out_dir):
    with open(out_dir, "w") as out:
        for num in ls:
            i,j,k,l = index[num]
            temp = process_text(data['data'][i]['paragraphs'][j]['qas'][k]['answers'][l]['text'].strip())
            out.write(temp+'\n')


#Question generator         
def generator_question(ls, index, out_dir):
    with open(out_dir, "w") as out:
        for num in ls:
            i,j,k,_ = index[num]
            temp = process_text(data['data'][i]['paragraphs'][j]['qas'][k]['question'].strip())
            out.write(temp+'\n')

#Entity generator    
def generator_entity(ls, index, out_dir):
    with open(out_dir, "w") as out:
        for num in ls:
            i,j,k,l = index[num]
            temp = process_text(data['data'][i]['paragraphs'][j]['qas'][k]['answers'][l]['entity'])
            if temp == '':
                temp = '<UNDEFINED>'
            out.write(temp+'\n')
            
#Question Type generator         
def generator_question_type(ls, index, out_dir):
    with open(out_dir, "w") as out:
        for num in ls:
            i,j,k,_ = index[num]
            temp = process_text(data['data'][i]['paragraphs'][j]['qas'][k]['question_type'])
            out.write(temp+'\n')            
            
#idx generator         
def generator_idx(ls, index, out_dir):
    with open(out_dir, "w") as out:
        for num in ls:
            i,j,k,l = index[num]
            temp =  str(i)+" "+str(j)+" "+str(k)+" "+str(l)
            out.write(temp+'\n')  


#Shuffle around a list of QA pairs, and pick top "percent" of pairs and store selected pairs in return list  
def shuffler_selctor(ls, index_note, percent, shuffle = False):
    temp = []
    total = 0
    index = dict()
    
    for num in ls:
        i,j = index_note[num]
        for k in range (len(data['data'][i]['paragraphs'][j]['qas'])):
            for l in range (len(data['data'][i]['paragraphs'][j]['qas'][k]['answers'])):
                index[total] = [i,j,k,l]
                total +=1
            
    temp = list(range(total))
    random.seed(1)
    if shuffle:
        random.shuffle(temp)
    
    return (temp[:int(total*percent)],index)
        

#Main function
def main(percent = 0.05):
    index_note = dict()
    dataset = 'relation_5'
    
    # #Count the total #QA pairs and #clinical-notes
    note_total=0
    for i in range (len(data['data'])):
        for j in range (len(data['data'][i]['paragraphs'])):
            index_note[note_total] = [i,j]
            note_total += 1
    
    #Preperation for shuffling the text
    ls_note = list(range(note_total))
    random.seed(1)
    ls_note = random.sample(ls_note, len(ls_note))
    
    ls_note_train = ls_note[:int(note_total*0.8)]
    ls_note_dev = ls_note[int(note_total*0.8):int(note_total*0.9)]
    ls_note_test = ls_note[int(note_total*0.9):]

    ls_train, index_train = shuffler_selctor(ls_note_train, index_note, percent)
    ls_dev, index_dev = shuffler_selctor(ls_note_dev, index_note, percent)
    ls_test, index_test = shuffler_selctor(ls_note_test, index_note, percent)
    
    
    #Generate src
    generator_answer(ls_train, index_train, out_dir = "../emrQG/"+dataset+"/train.src.pre")
    generator_answer(ls_dev, index_dev, out_dir = "../emrQG/"+dataset+"/dev.src.pre")
    generator_answer(ls_test, index_test, out_dir = "../emrQG/"+dataset+"/test.src.pre")
    
    #Generate tgt
    generator_question(ls_train, index_train, out_dir = "../emrQG/"+dataset+"/train.tgt.pre")
    generator_question(ls_dev, index_dev, out_dir = "../emrQG/"+dataset+"/dev.tgt.pre")
    generator_question(ls_test, index_test, out_dir = "../emrQG/"+dataset+"/test.tgt.pre")
    
    #Generate Entity
    generator_entity(ls_train, index_train, out_dir = "../emrQG/"+dataset+"/train.entity.pre")
    generator_entity(ls_dev, index_dev, out_dir = "../emrQG/"+dataset+"/dev.entity.pre")
    generator_entity(ls_test, index_test, out_dir = "../emrQG/"+dataset+"/test.entity.pre")
    
    #Gnerate idx
    generator_idx(ls_train, index_train, out_dir = "../emrQG/"+dataset+"/train.idx.pre")
    generator_idx(ls_dev, index_dev, out_dir = "../emrQG/"+dataset+"/dev.idx.pre")
    generator_idx(ls_test, index_test, out_dir = "../emrQG/"+dataset+"/test.idx.pre")
    
if __name__ == "__main__":
    main()