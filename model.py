import csv

class AffectationPPTI :
    
    
    def __init__(self,InFileName):
        self.filename = InFileName
        self.nbH = list()
        self.hCumule = list()
        self.disponibilites = [ dict () for i in range(31)]
        self.x_var = list()

    def read_InPut_file(self):
        i = 0
        with open(self.filename,newline='') as csvfile :
            dreader = csv.DictReader(csvfile)
            header = dreader.fieldnames
            
            for row in dreader : 
                
                #Disponibilites
                if len(row[header[0]]) == 0 :
                    nbh_tmp = row[header[2]]
                    
                    #Jour ferie, pas d'heure de travail
                    if float(nbh_tmp) == 0 or nbh_tmp == '':
                        self.nbH.append(0)
                        continue
                    #Jour de travail
                    elif float(nbh_tmp) > 0 : 
                        self.nbH.append(float(nbh_tmp))
                    
                    #Creer une variable pour chaque etudiant disponible au jour i tel jour
                    var_created = { c : 0 for c in header[3:] }    
                    for j in header[3:]:
                        if row[j] == "TRUE" :
                            var_created[j] = 1
                    
                    self.disponibilites[i] = var_created
                    i += 1

                #Recuperer les heures cumulees de chaque etudiant
                elif len(row[header[0]] != 0):
                    for j in header[3:] :
                        self.hCumule[j] = float(row[j])
                    break
                
                
            
    
    def write_OutPut_file(self, OutFileName):
        
        s = ""
        for x_day in self.x_var :
            
            for x in x_day :
                if x.x > 0 :
                  s += "M,"
            s += "\n"
        
        f = open(OutFileName, "a")
        f.write(s)
        f.close()
        
        
    
    def Solve_Model(self):
        pass





#if __name__ == '__main__':
#    
#    read_InPut_file()
#    
#    
#    Solve_Model()
#    
#    
#    write_OutPut_file()
#    

