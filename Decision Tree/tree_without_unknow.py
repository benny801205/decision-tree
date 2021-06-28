# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 14:20:49 2020

@author: Ping Cheng Chung
"""

import csv
import collections
import math 
import copy





def ComputePreInfoGain(data,label):
    dic=collections.defaultdict(list)
    for i in range(0,len(data)):
        dic[data[i]].append(label[i])
    sum=0.0
    length=len(data)
    
    
    for key in dic:
        n=len(dic[key])
        sum+=(algorithm(dic[key]))*(n/length)
    return sum

def GiniIndex(label):
    label_values=feature_dic["label"]
    length=len(label)
    if length==0:
        return 0
    sum=0.0
    for str in label_values:
        event_number=label.count(str)
        p=event_number/length
        sum+= p**2 
    
    return 1-sum
    
    
def MajorityError(label):
    label_values=feature_dic["label"]
    length=len(label)
    
    if length==0:
        return 0
    min_counter=-1
    
    for str in label_values:
        event_number=label.count(str)
        if event_number ==0:
            return 0
        if event_number < min_counter or min_counter < 0:
            min_counter=event_number
    return min_counter/length


def Entropy(label):
    label_values=feature_dic["label"]
    length=len(label)
    if length==0:
        return 0
    sum=0.0
    #print("new compute")
    for str in label_values:
        event_number=label.count(str)
        p=event_number/length
        #print("p=",p)
        if event_number==0:
            continue
        sum+= (-p)*math.log(p,2)
    #print("sum=",sum)
    return sum


def Pcik_Feature(candatate_list,data,label,depth):
    #print("depth",depth)
    node=Mynode()
    #print("d=",depth)
    #print((node.dictionary).keys())
    num,val=findMajornityNumber(label)
    if num==len(label) or len(candatate_list)==1 or depth >= Max_depth:
        #print(val)
        node.name=val
        node.result=True
        return node
    
    
    
    
    max_ig=-1
    dataindex=-1;
    s=algorithm(label)
    #print(candatate_list)
    for i in candatate_list:
        prs=s-ComputePreInfoGain(data[i],label)
        #print("prs=",prs)
        if prs > max_ig :
            max_ig=prs
            dataindex=i
    
    
    
    node.name=index_to_feature[dataindex]
    
    #print(index_to_feature[dataindex])
    ls=candatate_list.copy()
    ls.remove(dataindex)
    

    data_dic=collections.defaultdict(list);
    label_dic=collections.defaultdict(list);
    
    for value in feature_dic[node.name]:
        data_dic[value]=[]
        for i in range(0,len(feature_dic)):
            data_dic[value].append([])
        
    for i in range(0,len(label)):
        for h in range (0,14):
            #print("i",i)
            #print("h",h)



            pre=data_dic[(data[dataindex])[i]]
            if(len(pre)==0):
                for k in range(0,15):
                    pre.append([])
                
                
            (data_dic[(data[dataindex])[i]])[h].append((data[h])[i])

        label_dic[(data[dataindex])[i]].append(label[i])
        # build new branch
        
    #print("nodename",node.name)
    #print("featrues:",feature_dic[node.name])
    for value in feature_dic[node.name]:
        #print("value=",value)
        if len(label_dic[value])==0:
            #print('if')
            n,v=findMajornityNumber(label)
            #print("val=",v)
            end_node=Mynode()
            end_node.name=v
            end_node.result=True
            node.dictionary[value]=end_node
            #print((node.dictionary).keys())
        else:
            #print('else')
            #print('depth=',depth)
            node.dictionary[value]=Pcik_Feature(ls,data_dic[value],label_dic[value],depth+1)
            #print((node.dictionary).keys())

      #  print(label_dic[value])
       # print("value=",value)
        
    
    #print(node.name)
    return node





def findMajornityNumber(label):
    if len(label)==0:
        return 0,"hahaha"
    
    
    
    max_number=-1
    result=""
    for value in feature_dic['label']:
        n=label.count(value)
        if n > max_number:
            result=value
            max_number=n
    return max_number,result



class Mynode:
    def __init__(self):
        self.name = ""
        self.dictionary = dict()
        self.result=False





def FindResult(dataline,node):
    current_node=copy.deepcopy(node)
    
    while not current_node.result:
        #print("key=",current_node.dictionary.keys())
        index=feature_to_index[current_node.name]
        #test=current_node.dictionary

        current_node= current_node.dictionary[dataline[index]]
    return current_node.name


def NumericalAttribute(l):
    copyone=l.copy()
    copyone.sort()
    
    medium_index=math.floor(len(copyone)/2)
    medium_value=copyone[medium_index];
    
    #print("m=",medium_value)
    for i in range(0,len(l)):
        v=l[i]
        if v> medium_value :
            l[i]="1"
        else:
            l[i]="0"
    return  medium_value


def hanldeUknow(l,index):
    n,v=findreplacUknow(l,index)
    
    for i in range(0,len(l)):
        
        if l[i]=="?":
            l[i]=v
        
    return v

def findreplacUknow(label,index):
    if len(label)==0:
        return 0,"hahaha"

    max_number=-1
    result=""
    thisfeature=index_to_feature[index]
    for value in feature_dic[thisfeature]:
        n=label.count(value)
        if n > max_number:
            result=value
            max_number=n
    return max_number,result


"""

set the depth of the tree, and set the algorithm:Entropy, MajorityError,GiniIndex

and this file will read data-desc.csv which I made for input the label and features.
the file is in car folder.

"""
Max_depth=7;
algorithm=Entropy
#algorithm=GiniIndex
#algorithm=MajorityError


#need  numerical attributes index  0,2,4,10,11,12  swith to 0 and 1
NA_index=[0,2,4,10,11,12]
UK_index=[1,6,13]



index_to_maj=dict()
index_to_medium=dict()
data_list=[];
feature_dic=collections.defaultdict(list);
index_to_feature=collections.defaultdict();
feature_to_index=collections.defaultdict(int);
while(len(data_list)<15):
    data_list.append([]);
    

datatest=[]

# read train data
with open ( r"train_final.csv" , 'r' ) as f :
    line_counter=1
    for line in f :
        if(line_counter==1):
            line_counter=line_counter+1
        
        else:
            line_counter=line_counter+1
            terms = line.strip().split(',' )
            datatest=terms##
            for i in range(0,15):
                data_list[i].append(terms[i])


f.close();

##########################################################
# read label and feature list
### index 1,6,13 with unknow(?)
feature_dic['age']=['0','1']
feature_to_index['age']= 0
index_to_feature[0]='age'


strr='Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked'
feature_dic['workclass']=strr.replace(' ','').split(',')
feature_to_index['workclass']= 1
index_to_feature[1]='workclass'


feature_dic['fnlwgt']=['0','1']
feature_to_index['fnlwgt']= 2
index_to_feature[2]='fnlwgt'


strr='Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool'
feature_dic['education']=strr.replace(' ','').split(',')
feature_to_index['education']= 3
index_to_feature[3]='education'



feature_dic['education-num']=['0','1']
feature_to_index['education-num']= 4
index_to_feature[4]='education-num'


strr='Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse'
feature_dic['marital-status']=strr.replace(' ','').split(',')
feature_to_index['marital-status']= 5
index_to_feature[5]='marital-status'



strr="Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces"
feature_dic['occupation']=strr.replace(' ','').split(',')
feature_to_index['occupation']= 6
index_to_feature[6]='occupation'

strr='Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried'
feature_dic['relationship']=strr.replace(' ','').split(',')
feature_to_index['relationship']= 7
index_to_feature[7]='relationship'

strr='White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black'
feature_dic['race']=strr.replace(' ','').split(',')
feature_to_index['race']= 8
index_to_feature[8]='race'


strr='Female, Male'
feature_dic['sex']=strr.replace(' ','').split(',')
feature_to_index['sex']= 9
index_to_feature[9]='sex'


feature_dic['capital-gain']=['0','1']
feature_to_index['capital-gain']= 10
index_to_feature[10]='capital-gain'


feature_dic['capital-loss']=['0','1']
feature_to_index['capital-loss']= 11
index_to_feature[11]='capital-loss'



feature_dic['hours-per-week']=['0','1']
feature_to_index['hours-per-week']= 12
index_to_feature[12]='hours-per-week'


strr='United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands'
feature_dic['native-country']=strr.replace(' ','').split(',')
feature_to_index['native-country']= 13
index_to_feature[13]='native-country'



strr='0,1'
feature_dic['label']=strr.replace(' ','').split(',')
feature_to_index['label']= 14
index_to_feature[14]='label'



##############################################################

#Numerical Attribute data

for i in NA_index:
    
    v=NumericalAttribute(data_list[i])
    index_to_medium[i]=v


#handle uknow

for i in UK_index:
    v=hanldeUknow(data_list[i],i)
    #print(v)
    index_to_maj[i]=v


#print(feature_dic["label"]);

#feature index
ls=[0,1,2,3,4,5,6,7,8,9,10,11,12,13]
decision_tree=Pcik_Feature(ls,data_list,data_list[len(data_list)-1],0)
#print(datatest)
print("Start compute prediction error")

#print(decision_tree.dictionary['0'].name)



#Official submited print
number_counter=0
error_counter=0


preidsct_list=[]

with open ( r"test_final.csv" , 'r' ) as f :
    tar=1
    for line in f :
        if tar==1:
            tar=tar+1
            continue

        terms = line.strip().split(',' )
        ID=terms[0];
        terms=terms[1:]
        tar=tar+1
        for i in NA_index:
            aim=terms[i]
            medium=index_to_medium[i]
            if aim > medium:
                terms[i]="1"
            else:
                terms[i]="0"
                
        
        for i in UK_index:
            aim=terms[i]
            if aim =="?":
                terms[i]=index_to_maj[i]
        
        
        
                
        print("at line ", tar)    
        expect_answer=FindResult(terms,decision_tree)
        preidsct_list.append(expect_answer)
f.close();





with open('Kaggle_v1.csv', mode='w',newline='') as csv_file:
    fieldnames = ['ID', 'Prediction']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    for i in range(len(preidsct_list)):
        writer.writerow({'ID': i+1, 'Prediction': preidsct_list[i]})
    
    
    
csv_file.close();

































