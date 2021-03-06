import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

f=open("o.txt","r",encoding="utf8")
orig=f.read().replace("\n"," ")
f.close()

f2=open("s.txt","r",encoding="utf8")
plag=f2.read().replace("\n"," ")
f2.close()

#word tokenisation
tokens_o=word_tokenize(orig)
tokens_p=word_tokenize(plag)

#stop word removal
#punctuation removal
#stop_words=['তাই','সুতরাং','তথাপি','অধিকন্তু','অতএব','পরিশেষে','যদিও','অবশেষে','এখন','তবে','হওয়া','যেমন','তেমন','হইতে','হতে','থেকে','চেয়ে']
stop_words=[]
punctuations=['"','.','(',')',',',';',':',"''",'``']
#punctuations=[]
tokens_o = [w for w in tokens_o if not w in stop_words and not w in punctuations]
tokens_p = [w for w in tokens_p if not w in stop_words and not w in punctuations]
print(tokens_o)
print(tokens_p)

#Trigram Similiarity measures
trigrams_o=[]
for i in range(len(tokens_o)-2):
    t=(tokens_o[i],tokens_o[i+1],tokens_o[i+2])
    trigrams_o.append(t)

s=0
trigrams_p=[]
for i in range(len(tokens_p)-2):
    t=(tokens_p[i],tokens_p[i+1],tokens_p[i+2])
    trigrams_p.append(t)
    if t in trigrams_o:
        s+=1

print('Document plagiarism ->')

#jaccord coefficient = (S(o)^S(p))/(S(o) U S(p))
J=s/(len(trigrams_o)+len(trigrams_p)) 
print('By using Jaccord Coefficient Method:',J*100,'%')

#containment measure
C=s/len(trigrams_p)
print('By using Containment Measure Method:',C*100,'%')

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



# Sentence Tokenization - Custom Approach
def sentence_tokenize(word_tokens):
    words = ''
    sentence = []
    for word in word_tokens:
        if '।' in word or '?' in word: 
            words = words + ' ' + word
            sentence.append(words)
            words = ''
        else:
            if len(words)==0:
                words = word
            else: 
                words = words + ' ' + word
    return sentence


sent_o=sentence_tokenize(tokens_o)
sent_p=sentence_tokenize(tokens_p)

print(sent_o)
print(sent_p)


#maximum length of LCS for a sentence in suspicious text
max_lcs=0
sum_lcs=0

for i in sent_p:
    for j in sent_o:
        l=lcs(i,j)
        max_lcs=max(max_lcs,l)
    sum_lcs+=max_lcs
    max_lcs=0

score=sum_lcs/len(tokens_p)
print('By using Longest Common Subsequence:',score*100,'%')
