import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

f=open("English_original.txt","r")
orig=f.read().replace("\n"," ")
f.close()

f2=open("English_suspicious.txt","r")
plag=f2.read().replace("\n"," ")
f2.close()

#word tokenisation
tokens_o=word_tokenize(orig)
tokens_p=word_tokenize(plag)

#lowerCase
tokens_o = [token.lower() for token in tokens_o]
tokens_p = [token.lower() for token in tokens_p]

print(tokens_o)
print(tokens_p)
tokenss_p = tokens_p

#stop word removal
#punctuation removal
stop_words=set(stopwords.words('english'))
punctuations=['"','.','(',')',',','?',';',':',"''",'``']
tokens_o = [w for w in tokens_o if not w in stop_words and not w in punctuations]
tokens_p = [w for w in tokens_p if not w in stop_words and not w in punctuations]

print(tokens_o)
print(tokens_p)


#Trigram Similiarity measures
trigrams_o=[]
for i in range(len(tokens_o)-2):
    t=(tokens_o[i],tokens_o[i+1],tokens_o[i+2])
    trigrams_o.append(t)

print(trigrams_o)

s=0
trigrams_p=[]
for i in range(len(tokens_p)-2):
    t=(tokens_p[i],tokens_p[i+1],tokens_p[i+2])
    trigrams_p.append(t)
    if t in trigrams_o:
        s+=1

print(trigrams_p)

#jaccord coefficient = (S(o)^S(p))/(S(o) U S(p))
J=s/(len(trigrams_o)+len(trigrams_p)) 
print(J)

#containment measure
C=s/len(trigrams_p)
print(C)

#longest common subsequence
#dynamic programming algorithm for finding lcs
def lcs(l1,l2):
    s1=word_tokenize(l1)
    s2=word_tokenize(l2)
    # storing the dp values 
    dp = [[None]*(len(s1)+1) for i in range(len(s2)+1)] 
  
    for i in range(len(s2)+1): 
        for j in range(len(s1)+1): 
            if i == 0 or j == 0: 
                dp[i][j] = 0
            elif s2[i-1] == s1[j-1]: 
                dp[i][j] = dp[i-1][j-1]+1
            else: 
                dp[i][j] = max(dp[i-1][j] , dp[i][j-1]) 
    return dp[len(s2)][len(s1)]

sent_o=sent_tokenize(orig)
sent_p=sent_tokenize(plag)
print(sent_o)
print(sent_p)

#maximum length of LCS for a sentence in suspicious text
max_lcs=0
sum_lcs=0

for i in sent_p:
    for j in sent_o:
        l=lcs(i,j)
        print(l)
        max_lcs=max(max_lcs,l)
    sum_lcs+=max_lcs
    max_lcs=0

score=sum_lcs/len(tokenss_p)
print(score)
