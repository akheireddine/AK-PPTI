import csv
import sys
#from gurobipy import *


class AffectationPPTI :
    
    
    def __init__(self,InFileName):
        self.fileIN = InFileName
        self.fileOUT = "Unknown.txt"
        self.idEtudiant = list()
        self.nbH = dict()                        #cle : num_jour, valeur : nombre d'heure
        self.hCumule = dict()                    #cle : id_etudiant, value : (float) nombre d'heures cumulees de l'annee
        self.disponibilites = dict()             #cle : id_etudiant, value : (list) date de disponibilites (0,...,31)
        self.x_var = dict()                      #cle : num_jour, value : (list) des etudiants disponibles
        
        
        ################# LAUNCH RESOLUTION ################
        self.read_InPut_file()
#        self.Solve_Model()
#        self.write_OutPut_file()
        ################# LAUNCH RESOLUTION ################

        
        
        
        

    def read_InPut_file(self):
        j = 0
        i = -1
        end = False
        with open(self.fileIN) as csvfile :
            dreader = csv.DictReader(csvfile)
            header = dreader.fieldnames
            
            self.idEtudiant = header[3:]
            self.disponibilites = {etu : list() for etu in self.idEtudiant}
            self.hCumule = {etu : 0 for etu in self.idEtudiant}
            
            for row in dreader : 
                i += 1
                #fileOut name : last line of csv file
                if end :
                    self.fileOUT = row[header[2]]+"_Affectation"
                    break
                    
                    
                #Disponibilites
                if len(row[header[0]]) == 0 :
                    nbh_tmp = row[header[2]]
                    
                    index_virgule = nbh_tmp.find(",") 


                    if index_virgule != -1 : 
                        nbh_tmp = nbh_tmp.replace(',','.')
                        
                    
                    #Jour ferie, pas d'heure de travail
                    if len(nbh_tmp) == 0 or float(nbh_tmp) == 0 :
#                        self.nbH.append(0)
                        continue
                    #Jour de travail
                    elif float(nbh_tmp) > 0 : 
                        self.nbH[i] = float(nbh_tmp)
                        
                    
                    #Creer une variable pour chaque etudiant disponible au jour i tel jour
                    for etu in self.idEtudiant:
                        if row[etu] == "TRUE" :
                            self.disponibilites[etu].append(j)
                            
                    j += 1
                    
                #Recuperer les heures cumulees de chaque etudiant
                elif len(row[header[0]]) != 0:
                    for etu  in self.idEtudiant :
                        self.hCumule[etu] = float(row[etu])
                    end = True
                    

                    
            
    
    def write_OutPut_file(self):
        
        s = ""
        for num_j,etu_dispo_list in self.x_var.items() :
            
            for etu,xetu in etu_dispo_list.items() :
                if xetu.x > 0 :
                  s += etu+","
            s += "\n"
        
        f = open(self.fileOUT, "a")
        f.write(s)
        f.close()
        
        
    
    def Solve_Model(self):
        
#        
        try:
            m = Model("affectation")
            
            #CREER VARIABLE DU MODELE
            
            self.x_var = { c : dict() for c in self.nbH.keys() }
            
            for num_j in self.nbH.keys() : 
                
                for etu,dispo_etu in self.idEtudiant.items() :
           
                    if num_j in dispo_etu : 
                        self.x_var[num_j][etu] =  m.addVar(vtype=GRB.BINARY, name="x_"+etu+str(num_j) ) 
                    
                    
            
            
            #CREER LES CONTRAINTES DU MODELE
            
            
            #SEULEMENT DEUX ETUDIANT AFFECTE AU JOUR num_j
            for num_j, in self.nbH.keys() : 
                
                cst = LinExpr()
                for etu in self.idEtudiant :
                
                    if num_j in self.disponibilites[etu] :
                    
                        cst += self.x_var[num_j][etu]
                        
                
                m.addConstr(cst, GRB.EQUAL, 2 , "Only2Student")
            
            
            
            
            #UN ETUDIANT NE DOIT FAIRE QUE 25H PAR MOIS
            for etu in self.idEtudiant : 
                m.addConstr(quicksum([self.nbH[num_j] * self.x_var[num_j][etu] for num_j in self.nbH.keys()]),GRB.LESS_EQUAL, 25, "LIMIT_H_WORK")
                
                
            #FIXER L'OBJECTIVE
            m.setObjective(1, GRB.MAXIMIZE)
            
            #LANCER LE MODELE
            m.optimize()
    
            
        except GurobiError as e:
            print('Error code ' + str(e.errno) + ": " + str(e))
        
        except AttributeError:
            print('Encountered an attribute error')
#            
            
        pass



if __name__ == '__main__':
    
    if len(sys.argv[1:]) < 2 : 
        exit(1)
        
    Affectation = AffectationPPTI(sys.argv[1])
    
    
            
    print(Affectation.idEtudiant)
    print("\n")
    print(Affectation.disponibilites)
    print("\n")
    print(Affectation.hCumule)
    print("\n")
    print(Affectation.fileOUT)
    print("\n")
    print(Affectation.nbH)
        
