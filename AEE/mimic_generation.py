with open("./test_predictions.txt.NER", 'r') as pre_file, open('./test_predictions.txt.NER.post_processing', 'w') as mimic3_file:
    
    pre_lines = pre_file.readlines()
    
    label_count = 0
    num = 0

    start = False
    for i in range(len(pre_lines)):
        
        if pre_lines[i] != "\n":
            word = pre_lines[i].split()[0]
            label = pre_lines[i].split()[2]
            
            if label=="O":
                mimic3_file.write(" ".join([word,"O"])+"\n")
                start = False
            elif label=='I-Evidence':
                num+=1
                if start:
                    mimic3_file.write(" ".join([word,'I'])+"\n")
                else:
                    mimic3_file.write(" ".join([word,"B"])+"\n")
                    start = True
                    label_count += 1
            elif label=='B-Evidence':
                label_count += 1
                mimic3_file.write(" ".join([word,'B'])+"\n")
                start = True
                num+=1
                
            i+=1
        else:
            mimic3_file.write("\n")
    mimic3_file.write("\n")

    print(label_count)
    print(num)
    print(num/label_count)
    
            
            