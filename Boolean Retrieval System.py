from nltk.stem.porter import *
stemmer = PorterStemmer()
import tkinter as tk
from tkinter import *
from PIL import ImageTk


class GUI(Tk):
    def __init__(self): 
        Tk.__init__(self)
        self.tokken=[]
        self.tag=[]  
        self.inverted=dict()
        self.positional=dict() 
        
        self.preprocess()
        self.gui_generate()
    
    def gui_generate(self):
        self.image=ImageTk.PhotoImage(file="scrabble.jpg")
        self.label=Label(self, image=self.image)
        self.label.pack(fill=BOTH,expand=True)

        self.l=Label(self,text="Boolean Retreival Model", bg="white", fg="black" ,font="Courier 30 bold")
        # self.la=Label(self,text='', bg="black", fg="white",font="Courier 10", wraplength=400)
        self.entry=Entry(self,width=70,bd=3,font="Times_New_Roman 12")
        self.entry.bind("<Return>",self.queryProcess)
        self.f=Frame(self)
        self.b1=Button(self,text="Search",bg="white", bd=3,fg="black",font="Courier 15 bold")
        self.b1.bind("<Button-1>",self.queryProcess)

        self.b=Button(self,text="Exit",command=exit,bd=3,bg="white", fg="black",font="Courier 15 bold")
        self.v = Scrollbar(self.f)
        self.v.pack(side = RIGHT, fill = Y)
        self.t = Text(self.f,width = 100, height = 15, fg="white",bg="black",font="Cambria 10 bold",yscrollcommand = self.v.set)
        
        self.l.place(relx=0.25, rely=0.15,height=50)
        self.entry.place(relx=0.17, rely=0.35, height=35)
        self.b1.place(relx=0.73, rely=0.35)
        self.b.place(relx=0.92, rely=0.9)
        # self.la.place(relx=0,rely=0)
        self.f.place(relx=0,rely=0.5)
        self.f.place_forget()
        self.t.pack(side=TOP)
        self.v.config(command=self.t.yview)

    
    def preprocess(self):

        for i in range(1,51):
            f=open("./ShortStories/"+str(i)+ ".txt","r",encoding='utf-8')
            line=f.read().replace(","," ").replace("."," ").replace("?"," ").replace("!"," ").replace("“"," ").replace("”"," ").replace(";"," ").replace(":"," ").replace("’"," ").replace("‘"," ").replace("—"," ").replace("-"," ").replace("n’t","not").replace("\n"," ").replace("("," ").replace(")"," ").replace("*"," ").replace("["," ").replace("]"," ").lower().split()
            self.tokken.append(line)
            f.close()
            f=open("./ShortStories/"+str(i)+ ".txt","r",encoding='utf-8')
            self.tag.append(f.readline().replace("\n",""))
            f.close()
        stemmer = PorterStemmer()

        for i in range(len(self.tokken)):
            self.tokken[i]=[stemmer.stem(t) for t in self.tokken[i]]

        stopword1=open("./Stopword-List.txt","r",encoding='utf-8')
        stopword=stopword1.read()
        stopword1.close()
        


        for i in range(len(self.tokken)):
            for j in self.tokken[i]:
                index=[]
                if j not in stopword:
                    if j in self.inverted:
                        index=self.inverted[j]
                    if i+1 not in index:
                        index.append(i+1)
                    self.inverted[j]=index

        for key in self.inverted:
            self.positional[key] = {}
        n = 1
        for i in self.tokken:
            ind = 0
            for val in i:
                if val not in stopword:
                    if n not in self.positional[val]:
                        self.positional[val][n] = []
                    self.positional[val][n].append(ind)
                ind += 1
            n += 1

    def queryProcess(self,event):
        query=self.entry.get()
        search=[]
        connector=[]
        i=0
        n=[]
        number=[]
        query=query.replace("/","")

        query=query.split()
        query=[stemmer.stem(q) for q in query]
        for word in query:
            if word=="and" or word=="or" or word=="not":
                connector.append(word) 
            elif word.isdigit():
                number.append(word) 
            else:
                search.append(word)
            i+=1               
        doc=set()
        connector.append(" ") 

        if all(item in self.inverted.keys() for item in search):
            for i in range(1,51):
                doc.add(i)

            sett=set()
            
            if len(connector)>1:
                i=0   
                sett=set(self.inverted[search.pop(0)])

                for connect in connector:
                    if connect=="and" and i<len(connector):
                        if connector[i+1]=="not" : 
                            connector.pop(i)
                            a=set(self.inverted[search.pop()])
                            b=doc.difference(a)
                            sett=sett.intersection(b)
                        else:  
                            sett=sett.intersection(self.inverted[search.pop(0)])
                    elif connect=="or" and i<len(connector):
                        if connector[i+1] == "not": 
                            connector.pop(i)
                            a=set(self.inverted[search.pop()])
                            b=doc.difference(a)
                            sett.union(b)
                        else:
                            sett=sett.union(self.inverted[search.pop(0)])
                    elif connect =="not": 
                        sett=doc.difference(sett)
                    i+=1
            
            
            elif len(number)>0:
                a=set(self.inverted[search[0]])
                b=set(self.inverted[search[1]])
                c=a.intersection(b)
                t=int(number.pop(0))
                for i in c:
                    k=0
                    j=0
                    while j<len(self.positional[search[0]][i]) and k<len(self.positional[search[1]][i]):
                        if self.positional[search[0]][i][j]<self.positional[search[1]][i][k]:
                            if abs(self.positional[search[0]][i][j]-self.positional[search[1]][i][k])==t+1:
                                sett.add(i)
                            j+=1
                        elif self.positional[search[0]][i][j]>self.positional[search[1]][i][k]:
                            k+=1

                            
                
            else:
                sett=self.inverted[query[0]]
        
        else:
            sett={}

        if len(sett)>0:
            name=dict()
            for i in sett:
                name[i]=self.tag[i-1]
            self.f.place(relx=0,rely=0.5)
            self.t.delete('1.0', END)
            for i,j in name.items():
                self.t.insert(END,"Document#"+str(i)+"    "+"Story: "+str(j))
                self.t.insert(END,"\n")
        else:
            self.t.delete('1.0', END)
            self.t.insert(END,"No results found \n")
        






root=GUI()
root.title("Model")
root.geometry("1080x500")
root.mainloop()
