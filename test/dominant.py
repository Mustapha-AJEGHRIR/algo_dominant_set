import sys, os, time
import networkx as nx

from random import choices, random
from scipy.optimize import linprog


from sys import path as syspath

# ----------------------------------- PulP ----------------------------------- #
dir = "/".join(sys.argv[0].split('/')[:-1])
print(dir)
print(os.path.join(dir ,'PuLP-2.5.1'))
syspath.append(os.path.join(dir ,'PuLP-2.5.1'))
import pulp


# --------------------------------- Constants -------------------------------- #
SHOW = 0
DURATION = 2 #Duration for each round
REPETITIONS = 1000 #Max number of times you can restart random choices
PROBA = 0 #Proba of using dominant search
POWER = 5 #When chosing probilities, this helps to shap the choices

# ------------------------------------ ILP ----------------------------------- #
DURATION_ILP = 3


S = 0
START = time.time()
def dominant5(g_original : nx.classes.graph.Graph, name, f=[1]):
    start = time.time()
    weights : dict[int,int]= nx.get_node_attributes(g_original, 'weight')
    adjacency : list[list[int]] = []
    for i in range(len(weights)):
        adjacency.append(list(g_original.neighbors(i)))
    
    # ------------------------------------ ILP ----------------------------------- #
    model = pulp.LpProblem(name="small-problem", sense=pulp.LpMinimize)
    variables = []
    obj = 0
    for node in range(len(weights)): #Variables
        variables.append(pulp.LpVariable(name=str(node), lowBound=0, upBound=1, cat= "Integer"))
        obj += variables[node] * weights[node]
    model += obj
    for node in range(len(weights)): #Constraints
        constraint = variables[node]
        for neighbor in adjacency[node]:
            constraint += variables[neighbor]
        constraint = constraint >= 1
        model += constraint

    # print(pulp.listSolvers(onlyAvailable=True))
    # ---------------------------------- solver ---------------------------------- #
    solver = pulp.PULP_CBC_CMD(timeLimit=DURATION_ILP, msg=0)
    status = model.solve(solver)

    # ----------------------------------- Build ---------------------------------- #
    dom_set = []
    for var in model.variables():
        if var.value() == 1:
            dom_set.append(int(var.name))
    weight = 0
    for node in dom_set:
        weight += weights[node]
    
    print("*"*10, " For : ", name); f[0] += 1
    print("Min weight =", model.objective.value(), "\t", status, "\t", "Real weight =", weight)
    print(f"Total time = {(time.time() - start):.2f}s")
    return dom_set
    

def dominant4(g_original : nx.classes.graph.Graph, name, f=[1]):
    start = time.time()
    # ------------------------------- Solve the LP ------------------------------- #
    weights : dict[int,int]= nx.get_node_attributes(g_original, 'weight')
    total_edges_twice = 0
    adjacency : list[list[int]] = []
    for i in range(len(weights)):
        total_edges_twice += len(list(g_original.neighbors(i)))
        adjacency.append(list(g_original.neighbors(i)))
    
    obj : list[int] = [w for _,w in sorted(list(weights.items()))]  #The weights of our linear prog
    lhs_ineq : list[list[int]] = []                                 #Coefs of the inequalities "<="
    for node in range(len(weights)):
        one_lhs_ineq = [0]*len(weights)
        for neighbor in adjacency[node]:
            one_lhs_ineq[neighbor] = -1
        one_lhs_ineq[node] = -1
        lhs_ineq.append(one_lhs_ineq)
    rhs_ineq = [-1]*len(weights)                                     #Coefs of the right side "<= coef"
    bnd : list[(int,int)] = [(0, 1)]*len(weights)
    x0 = [1]*len(weights)
    opt : linprog() = linprog(c = obj, A_ub = lhs_ineq, b_ub = rhs_ineq, bounds = bnd , x0 = x0)
    dom_sets : list[set[int]] = []
    dom_weights : list[int]= []
    i = 0
    tic = time.time()
    while time.time() - tic < DURATION and i<REPETITIONS:
        i += 1
        dom_set :set[int] = set(range(len(weights)))
        X = 1-opt.x.copy()
        X **= POWER
        fails = 0
        coef = random()*5+1
        while fails < total_edges_twice/coef:
            try :
                worst :int = choices(list(enumerate(X)), weights=X)[0][0]
            except :
                break
            if (nx.is_dominating_set(g, dom_set.difference(set({worst})))):
                dom_set = dom_set.difference(set({worst}))
                X[worst] = 0
            else :
                fails += 1
        weight = 0
        for node in dom_set:
            weight += weights[node]
        dom_sets.append(dom_set)
        dom_weights.append(weight)
        if weight <= opt.fun:
            break

    dom_set = dom_sets[ dom_weights.index( min(dom_weights) ) ]
    # -------------------------------- Real weight ------------------------------- #
    weight = 0
    for node in dom_set:
        weight += weights[node]
    
    print("*"*10, " For : ", name); f[0] += 1
    print("its : ", i, "Min weight =", opt.fun, "\t", opt.success, "\t", "Real weight =", weight)
    print(f"Total time = {(time.time() - start):.2f}s")
    print()
    return dom_set




def dominant3(g_original : nx.classes.graph.Graph, name, f=[1]):
    start = time.time()
    # ------------------------------- Solve the LP ------------------------------- #
    weights : dict[int,int]= nx.get_node_attributes(g_original, 'weight')
    adjacency : list[list[int]] = []
    for i in range(len(weights)):
        adjacency.append(list(g_original.neighbors(i)))
    
    obj : list[int] = [w for _,w in sorted(list(weights.items()))]  #The weights of our linear prog
    lhs_ineq : list[list[int]] = []                                 #Coefs of the inequalities "<="
    for node in range(len(weights)):
        one_lhs_ineq = [0]*len(weights)
        for neighbor in adjacency[node]:
            one_lhs_ineq[neighbor] = -1
        one_lhs_ineq[node] = -1
        lhs_ineq.append(one_lhs_ineq)
    rhs_ineq = [-1]*len(weights)                                     #Coefs of the right side "<= coef"
    bnd : list[(int,int)] = [(0, 1)]*len(weights)
    x0 = [1]*len(weights)
    opt : linprog() = linprog(c = obj, A_ub = lhs_ineq, b_ub = rhs_ineq, bounds = bnd, x0 = x0)
    dom_sets : list[list[int]] = []
    dom_weights : list[int]= []
    i = 0
    tic = time.time()
    while time.time() - tic < DURATION and i<300:
        i += 1
        dom_set :list[int] = []
        X = opt.x.copy()
        X **= POWER
        while not nx.is_dominating_set(g_original, dom_set):
            best :int = choices(list(enumerate(X)), weights=X)[0][0]
            dom_set.append(best)
            X[best] = 0
            for neighbor in adjacency [best]:
                X[best] = 0
        weight = 0
        for node in dom_set:
            weight += weights[node]
        dom_sets.append(dom_set)
        dom_weights.append(weight)

    dom_set = dom_sets[ dom_weights.index( min(dom_weights) ) ]
    # -------------------------------- Real weight ------------------------------- #
    weight = 0
    for node in dom_set:
        weight += weights[node]
    
    print("*"*10, " For : ", name); f[0] += 1
    print("its : ", i, "Min weight =", opt.fun, "\t", opt.success, "\t", "Real weight =", weight)
    print(f"Total time = {(time.time() - start):.2f}s")
    print()
    return dom_set




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
        black_list : set[int] = set({})
        while not nx.is_dominating_set(g_original, dom_set):
            weights : dict[int,int]= nx.get_node_attributes(g, 'weight')    #dict(node) -> weigth
            degrees : list[(int, int)] = nx.degree(g)                       #list((node,deg))
            ratios : dict[int,int] = {}
            for node, deg in degrees :
                ratios[node] = (deg/weights[node])**POWER
                if node in black_list :
                    ratios[node] = 0
            ratios_items : list[(int, int)]= list(ratios.items())

            best :int = choices(ratios_items, weights=[w for _,w in ratios_items])[0][0]
            dom_set.append(best)
            g.remove_node(best)
            black_list = black_list.union(set(g_original.neighbors(best)))
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
    print("*"*10, " For : ", name); f[0] += 1
    print("Iterations = ", i, end ="\t")
    print("len of dom_set = ", len(dom_set), "\tTotal of nodes = ", len(g_original.nodes), "\tweight = ", min(dom_weights))
    # print("len of dom_set =", len(dom_set), "   nb of node =", len(g_original.nodes))
    # weight = 0
    # weights : dict[int,int]= nx.get_node_attributes(g_original, 'weight')    #dict(node) -> weigth
    # for node in dom_set:
        # weight += weights[node]
    # print("Weight was : ", weight)
    return dom_set



# def dominant(g : nx.classes.graph.Graph, first=[2]):
#     """
#         A Faire:         
#         - Ecrire une fonction qui retourne le dominant du graphe non dirigé g passé en parametre.
#         - cette fonction doit retourner la liste des noeuds d'un petit dominant de g

#         :param g: le graphe est donné dans le format networkx : https://networkx.github.io/documentation/stable/reference/classes/graph.html

#     """

#     if SHOW and first[0] > 0 :
#         nx.draw(g)
#         plt.show()
#         first[0] -= 1
#     # print(nx.info(g[0]))
#     return nx.dominating_set(g)

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
        D = sorted(dominant5(g, graph_filename), key=lambda x: int(x))
        # ajout au rapport
        weights = nx.get_node_attributes(g, 'weight')
        output_file.write(graph_filename)
        for node in D:
            output_file.write(' {}'.format(node))
            S += weights[node]
        output_file.write('\n')

    output_file.close()

print("Sum of weights = ", S)
print("Total time :", time.time() - START,"s")
