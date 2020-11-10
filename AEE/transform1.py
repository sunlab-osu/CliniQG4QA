with open('test_predictions.txt.NER.post_processing','r') as f, open('test_predictions.txt.NER.post_processing_1','w') as new_f:
    idx = 0
    printout =False
    chief_complaint = False
    
    for line in f:
        idx +=1
        if len(line.split())==2:
            if line.split()[0]=='.' and line.split()[1]=='B':
                printout=True
                new_f.write(line.split()[0]+" O\n")
            elif printout:
                printout=False
                new_f.write(line.split()[0]+" B\n")
            elif line.split()[0]=='chief':
                new_f.write(line.split()[0]+" B\n")
                chief_complaint = True
            elif line.split()[0]=='complaint:' and chief_complaint:
                new_f.write(line.split()[0]+" I\n")
            elif chief_complaint:
                new_f.write(line.split()[0]+" I\n")
                chief_complaint = False
            else:
                new_f.write(line)
            
        else:
            new_f.write(line)