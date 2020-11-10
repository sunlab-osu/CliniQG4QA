WINDOW_SIZE = 3
MIN_LEN = 3

with open('test_predictions.txt.NER.post_processing_1','r') as f:
    Q_len = {x:0 for x in range(1,21)}
    start = False
    start_id = 0
    count = 0
    line_num = 0
    
    doc_evidences = []
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
            if start:
                temp.append((start_id,line_num))
                start =False
                if count in Q_len:
                    Q_len[count] +=1
                else:
                    Q_len[20] +=1
                count = 0
            
            doc_evidences.append(temp)
            temp=[]
                
                
    print(Q_len)
    print(len(doc_evidences))
      
    prev = 0
    prev_len = 0
    
    doc_evidences_new=[]
    for doc in doc_evidences:
        for x in doc:
            length = x[1]-x[0]
            if length>=MIN_LEN :
                if x[0]-prev-prev_len<=WINDOW_SIZE and prev_len<MIN_LEN :
                    doc_evidences_new.append((prev,x[1]))
                    prev_len = x[1]-prev
                else:
                    doc_evidences_new.append(x)
                    prev = x[0]
                    prev_len=length

            else:
                if x[0]-prev-prev_len<=WINDOW_SIZE:
                    
                    last_one = doc_evidences_new[-1]
                    if last_one[0] == prev:
                        doc_evidences_new.pop()
                        doc_evidences_new.append((prev,x[1]))
                        prev_len = x[1]-prev
                    elif x[1]-prev>=MIN_LEN :
                        doc_evidences_new.append((prev,x[1]))
                        prev_len = x[1]-prev
                else:
                    prev=x[0]
                    prev_len = length
                    

    print(line_num)   
    doc_evidences_new.append((line_num,line_num))
    
with open('test_predictions.txt.NER.post_processing_1','r') as f, open('test_predictions.txt.NER.post_processing_2','w') as new_f:    
    old = f.readlines()
    evidence_advancer = 0
    for i in range(line_num):
        if old[i]!="\n":
            if i+1<doc_evidences_new[evidence_advancer][0]:
                new_f.write(old[i].strip().split()[0]+" O\n")
            elif i+1==doc_evidences_new[evidence_advancer][0]:
                new_f.write(old[i].strip().split()[0]+" B\n")
            elif i+1> doc_evidences_new[evidence_advancer][0] and i+1< doc_evidences_new[evidence_advancer][1]-1:
                new_f.write(old[i].strip().split()[0]+" I\n")
            elif i+1== doc_evidences_new[evidence_advancer][1]-1:
                new_f.write(old[i].strip().split()[0]+" I\n")
                evidence_advancer+=1
                # print(doc_evidences_new[evidence_advancer])
        else:
            new_f.write('\n')
    new_f.write('\n')
            

count = 0
num = 0
for x in Q_len:
    count+=Q_len[x]
    num += x*Q_len[x]
    
print("count: "+str(count))
print("avg len: "+str(num/count))
            
            
            
            
            
            
            
            
            
            
            
        