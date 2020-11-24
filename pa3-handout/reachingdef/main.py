import sys
import copy
import os
class Reaching:
    def __init__(self,file,out_file):
        self.data = [i.replace('\n', '') for i in open(file).readlines()]
        self.out_file=out_file
    def clean_data(self):
        for i in self.data:
            if i[0]=="p":
                self.data=self.data[self.data.index(i):]
                break
        self.V=self.data[0].split(" ")[1]

        self.B=[{'next':[]} for i in range(int(self.data[0].split(" ")[2]))]
        start=0
        self.B_mes=[]
        for i in self.data[1:]:
            if i[0]=='b':
                start+=1
                self.B_mes.append(i)
        for i in self.data[1:]:
            if i[0]=="e":
                mes=i.split(" ")
                start=int(mes[1])
                self.B[start-1]['next'].append(int(mes[2])-1)

    def start(self):
        out=[]
        entry=[[0 for j in self.B_mes] for i in range(len(self.B_mes))]
        for i in range(len(self.B_mes)):
            out.append([])
        change=None
        for i in range(len(out)):
            for j in range(len(out)):
                if i in self.B[j]['next']:
                    out[i].append(j)
        v_list=['q' for i in range(int(self.V))]

        c=len(self.B_mes)
        while change!=entry:
            change = copy.deepcopy(entry)
            
            for i in range(len(self.B_mes)):
                for j in out[i]:
                    pre=entry[j]
                    for q in range(len(pre)):
                        if pre[q]==1:entry[i][q]=1
                mes=self.B_mes[i].split(" ")
                if len(mes)>=3:
                    if mes[2]=='0':
                        pass
                    elif v_list[int(mes[2])-1]!='q':
                        kill_b=v_list[int(mes[2])-1]
                        v_list[int(mes[2]) - 1] = i
                        entry[i][kill_b] = 0
                        entry[i][i]=1
                    else:
                        v_list[int(mes[2])-1]=i
                        entry[i][i] = 1

        data=open(self.out_file,'w')
        for i in range(len(entry)):
            lista=[]
            for j in range(len(entry[i])):
                if entry[i][j]==1:
                    lista.append(j+1)
            text="rdout "+str(i+1)+" "+" ".join([str(q) for q in lista])+"\n"
            data.write(text)
if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit("The number of arguments is wrong, please try again")
    file, out_file = [os.path.abspath(os.path.realpath(n)) for n in sys.argv[1:3]]
    r=Reaching(file,out_file)
    r.clean_data()
    r.start()
