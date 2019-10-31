import csv
import sys

class AffectationPPTI :
    
    
    def __init__(self,InFileName,OutFileName):
        self.fileIN = InFileName
        self.fileOUT = OutFileName
        self.nbH = list()
        self.idEtudiant = list()
        self.hCumule = dict()                    #cle : id_etudiant, value : (float) nombre d'heures cumulees de l'annee
        self.disponibilites = dict()             #cle : id_etudiant, value : (list) date de disponibilites (0,...,31)
        self.x_var = list()                      #cle : id_etudiant, value : (list) variable du modele pour la date (0,...,31)
        
        
        
        ################# LAUNCH RESOLUTION ################
        self.read_InPut_file()
#        self.Solve_Model()
#        self.write_OutPut_file()
        ################# LAUNCH RESOLUTION ################

        
        
        
        

    def read_InPut_file(self):
        j = 0
        with open(self.fileIN) as csvfile :
            dreader = csv.DictReader(csvfile)
            header = dreader.fieldnames
            
            self.idEtudiant = header[3:]
            self.disponibilites = {etu : list() for etu in self.idEtudiant}
            self.hCumule = {etu : 0 for etu in self.idEtudiant}
            
            
            for row in dreader : 
                
                #Disponibilites
                if len(row[header[0]]) == 0 :
                    nbh_tmp = row[header[2]]
                    
                    index_virgule = nbh_tmp.find(",") 
                    print(index_virgule)
                    if index_virgule != -1 : 
                        nbh_tmp = nbh_tmp.replace(',','.')
                        
                    
                    print(len(nbh_tmp),nbh_tmp)
                    #Jour ferie, pas d'heure de travail
                    if len(nbh_tmp) == 0 or float(nbh_tmp) == 0 :
                        self.nbH.append(0)
                        continue
                    #Jour de travail
                    elif float(nbh_tmp) > 0 : 
                        self.nbH.append(float(nbh_tmp))
                    
                    #Creer une variable pour chaque etudiant disponible au jour i tel jour
                    for etu in self.idEtudiant:
                        if row[etu] == "TRUE" :
                            self.disponibilites[etu].append(j)
                            
                    j += 1

                #Recuperer les heures cumulees de chaque etudiant
                elif len(row[header[0]] != 0):
                    for etu  in self.idEtudiant :
                        self.hCumule[etu] = float(row[etu])
                    break
                
                
            
    
    def write_OutPut_file(self):
        
        s = ""
        for etu,xday_list in self.x_var.items() :
            
            for xday in xday_list :
                if xday.x > 0 :
                  s += etu+","
            s += "\n"
        
        f = open(self.fileOUT, "a")
        f.write(s)
        f.close()
        
        
    
    def Solve_Model(self):
        
        pass
        #CREER VARIABLE DU MODELE
        
        
        
        #CREER LES CONTRAINTES DU MODELE
        
        
        
        #LANCER LE MODELE
        
        
    
        





if __name__ == '__main__':
    
    if len(sys.argv[1:]) < 3 : 
        exit(1)
        
    Affectation = AffectationPPTI(sys.argv[1],sys.argv[2])
