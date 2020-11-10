import random

random.seed(55)

doc_evidences = []

with open('test_predictions.txt.NER.post_processing_2','r') as f:
    Q_len = {x:0 for x in range(1,21)}
    start = False
    start_id = 0
    count = 0
    line_num = 0
    

    temp = []
    for line in f:
        line_num += 1
        
        if len(line.split())==2:
            if line.split()[1]=='B' and count==0:
                start =True
                start_id = line_num
                count += 1
            elif line.split()[1]=='B' and count>0:
                temp.append((start_id,line_num))
                start =True
                start_id = line_num
                if count in Q_len:
                    Q_len[count] +=1
                else:
                    Q_len[20] +=1
                count = 1                
            elif line.split()[1]=='I':
                count += 1
            elif line.split()[1]=='O' and start:
                temp.append((start_id,line_num))
                
                start =False
                if count in Q_len:
                    Q_len[count] +=1
                else:
                    Q_len[20] +=1
                count = 0
                
        else:
            doc_evidences.append(temp)
            temp=[]
            
    doc_evidences.pop()            
    print(Q_len)
    print(doc_evidences[0])
    print(len(doc_evidences))
    print(doc_evidences[len(doc_evidences)-1])
    
count = 0
num = 0
for x in Q_len:
    count+=Q_len[x]
    num += x*Q_len[x]
    
print("count: "+str(count))
print("avg len: "+str(num/count))



    
