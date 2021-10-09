import sys, os, time
import networkx as nx
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash
import pylab as plt
from random import choices, random


# --------------------------------- Constants -------------------------------- #
SHOW = 0
DURATION = 5 #Duration for each round
PROBA = 0.001 #Proba of using dominant search
POWER = 15 #When chosing probilities, this helps to shap the choices

S = 0
def dominant2(g_original : nx.classes.graph.Graph, name, f=[1]):
    """
        A Faire:         
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

    """
    start = time.time()
    dom_sets : list[list[int]] = []
    dom_weights : list[int]= []
    i = 0
    while time.time() - start < DURATION:
        i+=1
        g : nx.classes.graph.Graph = g_original.copy()
        dom_set : list[int] = []
        while not nx.is_dominating_set(g_original, dom_set):
            weights : dict[int,int]= nx.get_node_attributes(g, 'weight')    #dict(node) -> weigth
            degrees : list[(int, int)] = nx.degree(g)                       #list((node,deg))
            ratios : dict[int,int] = {}
            for node, deg in degrees :
                ratios[node] = (deg/weights[node])**POWER
            ratios_items : list[(int, int)]= list(ratios.items())
            best :int = choices(ratios_items, weights=[w for _,w in ratios_items])[0][0]
            dom_set.append(best)
            g.remove_node(best)
            if PROBA > random(): #Abandon this and go for deterministic search to complete the already found stuff
                break
        if not nx.is_dominating_set(g_original, dom_set): # Make it domiante
            dom_set += list(nx.dominating_set(g))
        weight = 0
        weights : dict[int,int]= nx.get_node_attributes(g_original, 'weight')    #dict(node) -> weigth
        for node in dom_set:
            weight += weights[node]
        dom_weights.append(weight)
        dom_sets.append(dom_set)
    dom_set = dom_sets[ dom_weights.index( min(dom_weights) ) ]
    print("*"*10, " For : ", graph_filename); f[0] += 1
    print("Iterations = ", i, end ="\t")
    print("len of dom_set = ", len(dom_set), "\tTotal of nodes = ", len(g_original.nodes), "\tweight = ", min(dom_weights))
    print()
    # print("len of dom_set =", len(dom_set), "   nb of node =", len(g_original.nodes))
    # weight = 0
    # weights : dict[int,int]= nx.get_node_attributes(g_original, 'weight')    #dict(node) -> weigth
    # for node in dom_set:
        # weight += weights[node]
    # print("Weight was : ", weight)
    return dom_set



def dominant(g : nx.classes.graph.Graph, first=[2]):
    """
        A Faire:         
        - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
        - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

        :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

    """

    if SHOW and first[0] > 0 :
        nx.draw(g)
        plt.show()
        first[0] -= 1
    # print(nx.info(g[0]))
    return nx.dominating_set(g)

#########################################
#### Ne pas modifier le code suivant ####
#########################################


def load_graph(name):
    with open(name, "r") as f:
        state = 0
        G = None
        for l in f:
            if state == 0:  # Header nb of nodes
                state = 1
            elif state == 1:  # Nb of nodes
                nodes = int(l)
                state = 2
            elif state == 2:  # Header position
                i = 0
                state = 3
            elif state == 3:  # Position
                i += 1
                if i >= nodes:
                    state = 4
            elif state == 4:  # Header node weight
                i = 0
                state = 5
                G = nx.Graph()
            elif state == 5:  # Node weight
                G.add_node(i, weight=int(l))
                i += 1
                if i >= nodes:
                    state = 6
            elif state == 6:  # Header edge
                i = 0
                state = 7
            elif state == 7:
                if i > nodes:
                    pass
                else:
                    edges = l.strip().split(" ")
                    for j, w in enumerate(edges):
                        w = int(w)
                        if w == 1 and (not i == j):
                            G.add_edge(i, j)
                    i += 1

        return G


#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__ == "__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])

    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
        print(input_dir, "doesn't exist")
        exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
        print(output_dir, "doesn't exist")
        exit()

        # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    for graph_filename in sorted(os.listdir(input_dir)):
        # importer le graphe
        g = load_graph(os.path.join(input_dir, graph_filename))

        # calcul du dominant
        D = sorted(dominant2(g, graph_filename), key=lambda x: int(x))

        # ajout au rapport
        weights = nx.get_node_attributes(g, 'weight')
        output_file.write(graph_filename)
        for node in D:
            output_file.write(' {}'.format(node))
            S += weights[node]
        output_file.write('\n')

    output_file.close()

print("Sum of weights = ", S)
