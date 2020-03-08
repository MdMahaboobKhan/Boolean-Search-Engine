import sys
import operator

def my_tfidf(inv_index,line,resp,tfidf,opfile):
    final = []
    j = 0
    score = dict()
    line = line.rstrip()
    qterms = line.split(" ")
    for d in resp:
        score[d] = 0
        for t in qterms:
            if(d in inv_index[t]):
                score[d] += tfidf[d][t]

    ranked = sorted(score.items(), key = operator.itemgetter(1),reverse = True)

    for i in ranked:
        final.append(i[j])

    final_str = " ".join(final)
    # f = open(opfile,"a")
    # f.write("\nTF-IDF")
    # f.write("\nResults:"+str(final_str))
    return final_str
    
           

def my_And(inv_index,line,tfidf,opfile):
    query_dict = dict()
    resp = []
    count = 0
    line = line.rstrip()
    terms = line.split(" ")
    for term in terms:
        query_dict[term] = inv_index[term]
  
    for i in range(len(terms)-1):
        a = query_dict[terms[i]]
        b = query_dict[terms[i+1]]

        #check this condition
        if (count > 0):
            a = resp
        
        resp,count = intersect(a,b,count)

    #resp,count = intersect(query_dict,list(query_dict.keys()))
    resp_str = " ".join(resp)
    f = open(opfile,"a")
    f.write("DaatAnd")
    if(len(resp)>0):
        f.write("\n"+" ".join(terms))
        f.write("\nResults:"+" "+resp_str)
        f.write("\nNumber of documents in results:"+" "+str(len(resp)))
        f.write("\nNumber of comparisons:"+" "+str(count))
        tf = my_tfidf(inv_index,line,resp,tfidf,opfile)
        f.write("\nTF-IDF")
        f.write("\nResults:"+" "+tf)

    else:
        f.write("\n"+" ".join(terms))
        f.write("\nResults: empty")
        f.write("\nNumber of documents in results: 0")
        f.write("\nNumber of comparisons:"+str(count))
        f.write("\nTF-IDF")
        f.write("\nResults: empty")
    f.close()




def intersect(a,b,count):
    resp = []
    
    j = 0
    k = 0
    
    while(j<len(a) and k<len(b)):
        if(a[j] == b[k]):
            count = count+1
            resp.append(a[j])
            j = j+1
            k = k+1
        else:
            #print("here")
            count = count+1
            if(a[j]<b[k]):
                j = j+1
            else:
                k = k+1

    return resp,count




def my_or(inv_index,line,tfidf,opfile):
    query_dict = dict()
    count = 0
    resp = []
    line = line.rstrip()
    terms = line.split(" ")
    for term in terms:
        query_dict[term] = inv_index[term]

    for i in range(len(terms)-1):
        a = query_dict[terms[i]]
        b = query_dict[terms[i+1]]

        #check this condition
        if (count > 0):
            a = resp
        
        resp,count = union(a,b,count)
    #resp,count = union(query_dict,list(query_dict.keys()))
    resp_str = " ".join(resp)
    f = open(opfile,"a")
    f.write("\nDaatOr")
    if(len(resp)>0):
        f.write("\n"+" ".join(terms))
        f.write("\nResults:"+" "+str(resp_str))
        f.write("\nNumber of documents in results:"+" "+str(len(resp)))
        f.write("\nNumber of comparisons:"+" "+str(count))
        tf = my_tfidf(inv_index,line,resp,tfidf,opfile)
        f.write("\nTF-IDF")
        f.write("\nResults:"+" "+tf)
        f.write("\n")


    else:
        f.write("\n"+" ".join(terms))
        f.write("\nResults: empty")
        f.write("\nNumber of documents in results: 0")
        f.write("\nNumber of comparisons:"+" "+str(count))
        f.write("\nTF-IDF")
        f.write("\nResults: empty")
        f.write("\n")
    f.close()




def union(a,b,count):
    
    resp = []

    j = 0
    k = 0
    
    while(j<len(a) and k<len(b)):
        if(a[j] == b[k]):
            count = count+1
            resp.append(a[j])
            j = j+1
            k = k+1
        else:
            count = count+1
            if(a[j]<b[k]):
                resp.append(a[j])
                j = j+1
            else:
                resp.append(b[k])
                k = k+1
    
    while(j<len(a)):
        count = count + 1
        resp.append(a[j])
        j = j+1
    while(k<len(b)):
        count = count + 1    
        resp.append(b[k])
        k = k+1
    
    return resp,count




def inverted_index(file1):
    doc_count = 0
    my_dict = dict()
    doc_tf_dict = dict()
    tf_dict = dict()
    df_dict = dict()
    idf = dict()
    idf = dict()
    tfidf = dict()
    f = open(file1)

    for line in f:
        doc_count += 1
        line = line.rstrip()
        li = line.split("\t")
        doc_id = li[0]
        sent = li[1]
        #dict of dict to calc tf
        doc_tf_dict[doc_id] = dict()
        words = sent.split(" ")
        for word in words:
            idf[word] = 0
            #add term frequency
            if word not in doc_tf_dict[doc_id]:
                doc_tf_dict[doc_id][word] = 1
            else:
                doc_tf_dict[doc_id][word] += 1

            
            #add doc frequency for word
            if word not in df_dict:
                df_dict[word] = 1
            else:
                if(doc_id not in my_dict[word]):
                    df_dict[word] +=1
            
            #add the term to inverted index
            if word not in my_dict:

                my_dict[word] = []
                my_dict[word].append(doc_id)
            else:
                if(doc_id not in my_dict[word]):
                    my_dict[word].append(doc_id)
    
    #creating tfs as per requirement
    total_terms = dict()
    for d in doc_tf_dict:
        total_terms[d] = 0
        for t in doc_tf_dict[d]:
            total_terms[d] += doc_tf_dict[d][t]
    
    for d in doc_tf_dict:
        for t in doc_tf_dict[d]:
            doc_tf_dict[d][t] = doc_tf_dict[d][t]/total_terms[d]

    #idf dict
    all_terms = list(my_dict.keys())
    for w in all_terms:
        idf[w] = doc_count/df_dict[w]

    #tf-idf weights
    for d in doc_tf_dict:
        tfidf[d] = dict()
        for t in doc_tf_dict[d]:
            tfidf[d][t] = doc_tf_dict[d][t] * idf[t]



    return my_dict,df_dict,tfidf       


def get_postings(inv_index,term,opfile):
    f = open(opfile,"a")
    f.write("GetPostings\n")
    f.write(term+"\n")
    posting = " ".join(inv_index[term])
    f.write("Postings list:"+" "+posting)
    f.write("\n")
    f.close()


if __name__ == "__main__":

    #print(dfs)
    arguments = sys.argv
    inv_index, dfs, tfidf = inverted_index(arguments[1])
    with open(arguments[3]) as f:
        for line in f:
            line = line.rstrip()
            terms = line.split(" ")
            for term in terms:
                get_postings(inv_index,term,arguments[2])

            my_And(inv_index,line,tfidf,arguments[2])
            my_or(inv_index,line,tfidf,arguments[2])
            f1 = open(arguments[2],"a")
            f1.write("\n")
            f1.close()
    f.close()
    

