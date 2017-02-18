# coding=utf-8
# Variante d'algorithme : fonctions non dominantes
# Version utilisée Python 2.7 - Packages à installer python-tk,

from random import shuffle, randint
import time
from math import sqrt
import numpy
import sys


class Gene(object):
    """ This class define a gene. """

    def __init__(self):
        self.id = None          # identifiant du dictionnaire
        self.proximity = dict()  # dictionnaires de distances entre gènes
        self.expression = None  # expression
        self.access = ""        # numéro d'accession du gène
        self.chr = ""           # numéro du chromosome sur lequel est le gène
        self.x = None           # coordonnée x
        self.y = None           # coordonnée y
        self.z = None           # coordonnée z
        self.cluster = 0        # numéro du cluster auxquel appartient le gène

    def calculateProximity(self, geneb):
        """
        Calculate the distance between two genes with their coordinates.
        :param geneb:
        :return:
        """
        dist = sqrt((self.x - geneb.x) ** 2 + (self.y - geneb.y) ** 2 + (self.z - geneb.z) ** 2)
        return dist

    def __repr__(self):  # Fait un return de la classe
        return str(self.access)  # Si on affiche l'objet gene, on ne retourne que son id


    def print_result(self):
        return "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".format(self.access, self.chr, self.x, self.y, self.z,
                                                          self.expression, self.cluster)


class Chromosome(object):
    """ This class define a chromosome. """

    def __init__(self):
        self.genesDict = dict()             # Dictionnaire de gènes id:gene
        self.genesDictExprTemp = dict()     # Dictionnaire temporaire d'expression
        self.maxProximity = 0               # Distance maximale
        self.maxExpression = 0              # Expression maximale

    def fromfiles(self, path_coord=None, path_expr=None):
        """
        Read the data files with the functions fromFileExpr and fromFileCoord, then keep only ones who have the good id and an expression data to 48h.
        :param path_coord: path of the coordinates file
        :param path_expr: path of the expression file
        :return:
        """
        self.fromFileExpr(path_expr)
        self.fromFileCoord(path_coord)
        maxProximity = 0

        list_to_delete = []
        for gene in self.genesDict:
            if self.genesDict[gene].access in self.genesDictExprTemp:
                self.genesDict[gene].expression = self.genesDictExprTemp[self.genesDict[gene].access]
            else:
                list_to_delete.append(gene)

        for thing_to_delete in list_to_delete:
            del self.genesDict[thing_to_delete]

        for gene in self.genesDict:
            for geneb in self.genesDict:
                value = self.genesDict[gene].calculateProximity(
                    self.genesDict[geneb])  # Stocke dans le dictionnaire du gène a la distance au gène b
                if maxProximity < value:
                    maxProximity = value
                self.genesDict[gene].proximity[self.genesDict[geneb].id] = value
        for gene in self.genesDict:
            for geneb in self.genesDict:
                self.genesDict[gene].proximity[self.genesDict[geneb].id] /= maxProximity

    def fromFileCoord(self, path):
        """
        Reads the file and filled the dictionary " genesList " by matching the number of each gene with
        the corresponding dictionary and the list of similarities in the Gene class.
        :param path: Path of the file.
        :return: -
        """

        nb_genes = 1
        with open(path, "r+") as file:
            for line in file:
                try:
                    gene = Gene()
                    line = line.split()
                    gene.access = line[0]
                    gene.chr = line[1]
                    gene.x = float(line[2])
                    gene.y = float(line[3])
                    gene.z = float(line[4])
                    gene.id = nb_genes          # crée les id des gènes
                    self.genesDict[
                        nb_genes] = gene        # attribue un numéro aux gènes et stocke la valeur du gène dans le dictionnaire
                    nb_genes += 1
                except Exception as e:
                    print e

    def fromFileExpr(self, path):
        current_id = ""
        maxExpression = 0
        minExpression = sys.maxint

        with open(path, "r+") as file:
            for line in file:
                if line.startswith("Gene ID:"):
                    current_id = line[len("Gene ID:"):].strip(" \r\n,")
                if line.startswith("Pf-iRBC 48hr Max FC:"):
                    try:
                        current_expr = line[len("Pf-iRBC 48hr Max FC:"):].strip(" \r\n,")
                        self.genesDictExprTemp[current_id] = float(current_expr)
                        if maxExpression < float(current_expr):
                            maxExpression = float(current_expr)
                        if minExpression > float(current_expr):
                            minExpression = float(current_expr)
                    except Exception as e:
                        pass

        for current_id in self.genesDictExprTemp:
            self.genesDictExprTemp[current_id] = (self.genesDictExprTemp[current_id] - minExpression) / (maxExpression - minExpression)


class Individual(object):
    """ This class define the different methods for the genetic algorithm where an individual is one chromosome. """

    def __init__(self):
        self.individual = []  # Un individu (liste de clusters)
        self.mutationRate = 5  # Taux de mutation
        self.fitness1 = 0  # Fitness de densité
        self.fitness2 = 0  # Fitness de similarité
        self.fitness3 = 0  # Fitness générale

    def generate(self, listGenes, nb_clust):
        """
        Generates random individuals from a list of genes.
        :param listGenes: List of genes.
        :return: -
        """
        tempIndividual = listGenes.values()  # Copie les gènes pour créer le nouvel individu car shuffle a besoin d'une liste
        shuffle(tempIndividual)  # shuffle mélange aléatoirement la liste

        # Crée les clusters aléatoirement par insertion de "0" ; le nbr de 0 est proportionnel au nombre de gènes (5%)
        for i in range(0, (nb_clust * len(listGenes)) / 100):
            tempIndividual.insert(randint(1, len(tempIndividual) - 1), 0)
        self.individual = tempIndividual  # Sauvegarde la valeur d'individual

    def clustersWithout0(self):
        """
        Create a list of clusters without the 0 in order to be able to do the calculations above.
        :return:
        """
        clusters = []  # liste de clusters (individu)
        temp_list = []  # liste temporaire contenant un seul cluster

        for i in self.individual:  # pour chaque élément dans l'individu
            if i != 0:  # si l'élément est différent de 0
                temp_list.append(i)  # met cet élément dans la temp_list
            else:
                if temp_list:  # sinon si temp_list n'est pas vide (différent d'une liste vide)
                    clusters.append(temp_list)  # ajoute les éléments de temp_list à la liste de clusters
                temp_list = []  # vide temp_list
        if temp_list:  # si temp_list existe, ajoute temps_list si on n'a pas rencontré de 0 dans la boucle
            clusters.append(temp_list)
        return clusters

    def proximityFitness(self):
        """
        Calculates the fitness for gene density by calculating the average of the densities of genes for every cluster
        :return: Returns the total distance (or density).
        """
        clusters = []  # liste de clusters (individu)
        fitness = 0  # distance totale d'un individu initialisée à 0
        inner_proximity = []  # distance deux à deux des gènes d'un cluster

        # Crée une liste de clusters sans les 0
        clusters = self.clustersWithout0()

        # Calcule la moyenne des distances totales des individus d'un cluster
        for cluster in clusters:  # pour chaque cluster dans la liste de clusters
            for gene in cluster:  # pour chaque gène dans le cluster
                for genex in cluster:  # et pour tous les autres gènes dans le même cluster
                    inner_proximity.append(
                        gene.proximity[genex.id])  # crée la liste des distances deux à deux du gène à tous les autres
            averageProximity = sum(inner_proximity)  # fait la somme des distance deux à deux
            averageProximity /= 2.0  # on divise par 2 car on a calculé les distances a-x et x-a
            try:
                averageProximity /= len(cluster)  # on divise par la longueur du cluster pour avoir la distance moyenne
            except ZeroDivisionError:
                averageProximity = 0
            fitness += averageProximity  # calcule la distance totale pour l'individu
            inner_proximity = []  # réinitialise la moyenne des distances du cluster
        fitness /= len(clusters)  # calcule la moyenne des distances totale de l'individu
        self.fitness1 = fitness

    def expressionFitness(self):
        """
        Calculates the fitness for gene similarity by calculating the average standard deviation of the expression values of the individual.
        :return:
        """
        clusters = []  # liste de clusters (individu)
        fitness = 0  # Fitness finale d'expression
        temp_expr = []  # Valeurs d'expression des gènes d'un même cluster
        expr = 0

        # Crée une liste de clusters dans les 0
        clusters = self.clustersWithout0()

        # Calcule la somme minimale des écarts-types pour un cluster
        for cluster in clusters:  # pour chaque cluster dans la liste de clusters
            for gene in cluster:  # pour chaque gène dans le cluster
                temp_expr.append(gene.expression)  # ajoute la valeur d'expression du gène à la liste
            sigma = numpy.std(temp_expr)  # calcule l'écart-type des valeurs d'expression du cluster
            fitness += sigma  # somme l'écart-type du cluster
            temp_expr = []  # réinitialise la valeur d'expression du gène
        fitness /= len(clusters)  # calcule l'écart-type moyen des valeurs d'expression de l'individu
        self.fitness2 = fitness

    def generalFitness(self):
        """
        Calculates the general fitness combining the two previous to compare the different types of data.
        :return:
        """
        self.expressionFitness()
        self.proximityFitness()
        fitness = abs(self.fitness1 * self.fitness2)
        self.fitness3 = fitness

    def exchange(self, i1, i2):
        """
        Exchange the elements of the individual with i1 and i2 indexes. This function is a mutation process.
        :param i1: Gene a
        :param i2: Gene b
        """
        x = self.individual[i1]
        self.individual[i1] = self.individual[i2]
        self.individual[i2] = x

    def mutation(self):
        """
        Calculates the necessary mutation rate to prevent the algorithm remains blocked.
        :return: -
        """
        length = len(self.individual) - 1
        nbMut = (len(self.individual) * self.mutationRate) / 100  # Nbr de permutations à faire (nbr de gènes à modifier)
        for i in range(0, int(round(nbMut, 0))):  # Echange des gènes aléatoirement au sein d'un individu
            self.exchange(randint(0, length), randint(0, length))

    def __deepcopy__(self):
        """Replace the basic deepcopy function with a faster one. It assumes that the elements in the :attr:`values` tuple are
        immutable and the fitness does not contain any other object than :attr:`values` and :attr:`weights`.
        """
        copy_ = self.__class__()
        copy_.individual = self.individual[:]
        return copy_

    def __repr__(self):  # Fait un return de la classe
        return "Fitness1 : {0}  Fitness2 : {1}  Fitness3 : {2}  Individual : {3}   ".format(self.fitness1,
                                                                                            self.fitness2,
                                                                                            self.fitness3,
                                                                                            self.individual)


class GeneticAlgorithm(object):
    """ This class will manage the evolutive process."""

    def __init__(self, chromosome):
        self.initialMutationRate = 5  # Taux de mutation propre à chaque individu
        self.individualNumber = 20  # Nombre de chromosomes de départ
        self.newIndividualList = []  # Nouveaux individus créés après mutation
        self.chromosome = chromosome  # Permet de récupérer les valeurs correspondant au gène x
        self.nb_run = 50
        self.name_save_file = "result.txt"
        self.nb_clust = 5

    def run(self):
        """
        Steps of the genetic algorithm.
        :return: -
        """
        # Génération des individus de départ tant que la longueur de la liste d'individus est < à individuNumber
        bestFitness = sys.maxint  # Défini un nombre maximal de densité pour pouvoir chercher la valeur minimale d'une liste
        start_time = time.time()

        for i in range(0, self.nb_run):  # Nbombre de tours de l'algorithme
            # Gènère individualNumber=20 individus de départ
            for i in range(len(self.newIndividualList),
                           self.individualNumber):  # prend en compte les 5 meilleurs individus précédemment enregistrés
                my_individual = Individual()  # appelle la classe individu pour créer l'objet my_individual
                my_individual.generate(self.chromosome.genesDict, self.nb_clust)  # génère les individus à partir de genesList
                self.newIndividualList.append(my_individual)  # rempli la liste

            # Evaluation (boucle sur tous les individus testant la fitness générale, puis suppression des plus faibles).
            for subject in self.newIndividualList:
                subject.generalFitness()
            self.newIndividualList = sorted(self.newIndividualList, key=lambda
                x: x.fitness3)  # trie les individus en fonction de leur fitness et associe la valeur de fitness à l'individu correspondant
            temp_best = self.newIndividualList[0].__deepcopy__()  # sauvegarde le meilleur individu
            self.newIndividualList = self.newIndividualList[0:5]  # Conserve les 5 meilleurs individus

            # Mutation des individus
            for subject in self.newIndividualList:
                subject.mutationRate = self.initialMutationRate
                subject.mutation()
            self.newIndividualList.append(temp_best)  # remet le meilleur individu non muté dans la liste pour ne pas régresser

            # Impression des résultats lorsque la fitness est améliorée, et si elle ne s'améliore pas, elle augmente de 2% à chaque tour

            if bestFitness > self.newIndividualList[0].fitness3:
                print self.newIndividualList[0]
                bestFitness = self.newIndividualList[0].fitness3
                self.initialMutationRate = 5  # réinitialise le taux de mmutation à 0.05
            else:
                self.initialMutationRate += 2

        for subject in self.newIndividualList[0:1]:
            print subject

        # output.put(self.run)
        self.timer = time.time() - start_time

    def save(self, path):
        my_best_individual = self.newIndividualList[0]
        my_best_individual = my_best_individual.individual
        nb_cluster = 0
        for i in my_best_individual:
            if i != 0:
                self.chromosome.genesDict[i.id].cluster = nb_cluster
            else:
                nb_cluster += 1

        with open(path, "w+") as file:
            file.writelines("new_ID		    chr Xcoord	Ycoord	Zcoord  expression   cluster\n")
            for i in my_best_individual:
                if i != 0:
                    file.writelines(self.chromosome.genesDict[i.id].print_result() + "\n")


# Execution du code
if __name__ == '__main__':
    C = Chromosome()  # Crée un chromosome vide.
    C.fromfiles("coordinates_data1.1.txt", "final expression.txt")  # Rempli le chromosome (dictionnaire de gène) à partir des valeurs de gènes.
    G = GeneticAlgorithm(C)  # Crée un objet GeneticAlgorithm à partir du chromosome C
    G.run()  # Lance les méthodes de GeneticAlgorithm
    I = Individual()

