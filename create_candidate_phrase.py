import nltk
import re



# data is the list that contains the original documents
# To process multiple documents, store like following examples
data = ['english is shown to be trans context free on the basis of coordinations of the respectively type that involve strictly syntactic cross serial agreement the agreement in question involves number in nouns and reflexive pronouns and is syntactic rather than semantic in nature because grammatical number in english like grammatical gender in languages such as french is partly arbitrary the formal proof which makes crucial use of the interchange lemma of ogden is so constructed as to be valid even if english is presumed to contain grammatical sentences in which respectively operates across a pair of coordinate phrases one of whose members has fewer conjuncts than the other it thus goes through whatever the facts may be regarding constructions with unequal numbers of conjuncts in the scope of respectively whereas other arguments have foundered on this problem' ,'doc2', 'doc3']
# We will use 2 different regular expression to collect candidate noun phrases.
# First is "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}", and the second is , '"NP: {<DT>?<JJ>*<NN>}" 
# First can collect all noun phrases that have length of more than 2, but cannot collect noun phrase with length of 1
# Second can collect all noun itself plus adj + noun set (by JJ * NN)





##############################################################################################
###################First processing of generating noun phrases
# Regular Expression 
NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
#NP = "NP: {<DT>?<JJ>*<NN>}" 
#NP = r"NP: {(\w+ DT)? (\w+ JJ)* (\w+ (NN|NP|PRN))}"
chunkr = nltk.RegexpParser(NP)

tokens = [nltk.word_tokenize(i) for i in data]
tag_list = [nltk.pos_tag(w) for w in tokens]
phrases = [chunkr.parse(sublist) for sublist in tag_list]


######################First collected candidate noun phrase refining process
data_np = []
data_inter_np = []
for i in range(0,len(phrases)):
    for line in str(phrases[i]).split("\n"):
        if line.replace(" ","")[0:3] == "(NP":
            line = line.split()
            #print(line)
            np = []
            for item in line:
                if "/" in item:
                    np.append(item.split("/")[0])
            if len(np) !=0:
                np = " ".join(np)
                np = "".join(re.findall("[a-zA-Z 0-9]+",np)).lower()
                data_inter_np.append(np)
            #print(data_inter_np)
    data_inter_np = list(set(data_inter_np))
    data_np.append(data_inter_np)
    data_inter_np = []

#The first candidate noun phrases are contained in data_np list.

    
    
    
    
    
    
    
    
    

#################################################################################################
#############Second Processing for extract one length noun in the document
#NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
NP = "NP: {<DT>?<JJ>*<NN>}" 
#NP = r"NP: {(\w+ DT)? (\w+ JJ)* (\w+ (NN|NP|PRN))}"
chunkr = nltk.RegexpParser(NP)

tokens = [nltk.word_tokenize(i) for i in data]
tag_list = [nltk.pos_tag(w) for w in tokens]
noun_phrases = [chunkr.parse(sublist) for sublist in tag_list]

data_np_second = []
data_inter_np = []
for i in range(0,len(noun_phrases)):
    for line in str(noun_phrases[i]).split("\n"):
        if line.replace(" ","")[0:3] == "(NP":
            line = line.split()
            #print(line)
            np = []
            for item in line:
                if "/" in item:
                    np.append(item.split("/")[0])
            if len(np) !=0:
                np = " ".join(np)
                np = "".join(re.findall("[a-zA-Z 0-9]+",np)).lower()
                if len(np) >= 4:
                    if 'the' in np:
                        check_np = np.replace("the","")
                        if len(check_np)>=5:
                            data_inter_np.append(np)
                    else:
                        data_inter_np.append(np)
               
    data_inter_np = list(set(data_inter_np))
    data_np_second.append(data_inter_np)
    data_inter_np = []

######################Second collected candidate noun phrase refining process
second_refine_inter, second_refine = [], []
for i in range(0,len(data_np_second)):
    for element in data_np_second[i]:
        element = element.replace("a ","").replace("the ","").replace("an ","").replace("this ","")
        element = element.split()
        if len(element) >= 2:
            second_refine_inter.append(" ".join(element))
        else:
            if element[0] in " ".join(data_np[i]):
                pass
            else:
                if element[0] != 'amount' and element[0] != 'problem' and element[0] !='problems':
                    second_refine_inter.append(element[0])
    second_refine.append(second_refine_inter)
    second_refine_inter = []
data_np_second = second_refine


#The second noun candiate sets are stored in data_np_second










###################################################################################################
############################Final Candidate process is contained in the list 'kp'
kp = []
for a,b in zip(data_np, data_np_second):
    kp.append(a+b)

for item in kp:
    print(item)
