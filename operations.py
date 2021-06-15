import copy
import time
from AF import *


def supp_epsi_transition(A):
    A1 = Automate(A.alphabet, A.etats_init, A.etats, A.etats_final)
    for etat in A.etats:
        ferm = A.epsilon_fermeture(etat, etat)
        A1.add_etat(etat)
        for symbol in A.alphabet:
            dest = set()
            for e in ferm:
                a = A[e][symbol]
                if a != None:
                    if type(a) != type([]):
                        dest.add(a)
                    else:
                        dest.update(a)
            for d in dest:
                A1[etat].add_transition(symbol, d)
        if (ferm.intersection(A.etats_final) != set()) and etat not in A1.etats_final:
            A1.etats_final.append(etat)
    return A1


def determiniser(A):
    '''
    Permet de déterminiser un automate suivant l'explication du cours :
    on commence en construisant un ensemble constitué des états initiaux ,puis à partir de celui-ci, on construis les états de proche en proche par dtermination de la destination de chaque element de l'ensemble en lisant un certain symbole de l'alphabet
    '''
    final_states = []
    transitions = []
    if not A.est_deterministe():
        initial = set(A.etats_init)
        l = []
        l.append(set(initial))
        while len(l) != 0:
            etat_en_cours = l.pop(0)
            for symbol in A.alphabet:
                initial.clear()
                for e in etat_en_cours:
                    a = A[e][symbol]
                    if a != None:
                        if type(a) != type([]):
                            initial.add(a)
                        else:
                            initial.update(a)
                if initial != set():
                    t = (str(etat_en_cours),
                         symbol, str(initial))
                    if not t in transitions:
                        transitions.append(t)
                    if not initial in final_states:
                        l.append(set(initial))
            if not etat_en_cours in final_states:
                final_states.append(set(etat_en_cours))
        final = [
            str(etat) for etat in final_states if etat.intersection(A.etats_final) != set()
        ]
        etat = [str(etat) for etat in final_states]
        return Automate(A.alphabet, set(A.etats_init), etat, final, transitions)


def rendre_complet(A):
    '''
        Si l'automate n'est pas déterministe, le rendre détermiste ensuite, 
        si l'on se rend compte qu'il n'est pas complet alors créer un état puit et relier vers lui toute les transition manquante
    '''
    B = ''
    if A.spontanee:
        B = supp_epsi_transition(A)
    else:
        B = copy.deepcopy(A)
    if not B.est_deterministe():
        B = determiniser(B)
    if not B.est_complet():
        B.add_etat("puit")
        for symbol in B.alphabet:
            B["puit"].add_transition(symbol, "puit")
        for etat in B.etats:
            for symbol in B.alphabet:
                if B[etat][symbol] == None:
                    B[etat].add_transition(symbol, 'puit')
    return B


def main():
    alpha = "ab"
    etats = [0, 1, 2, 3, 4]
    transitions = [(0, 'a', 1), (0, mot_vide, 2), (1, mot_vide, 4),
                   (2, 'a', 3), (2, 'b', 3), (3, mot_vide, 4), (3, 'b', 2), ]

    init = [0]
    final = [4]
    A = Automate(alpha, init, etats, final, transitions)
    '''print(A[0])
   print(A.est_deterministe())
   print(A)
   B = copy.deepcopy(A)
   A.add_etat(3)
   print(B)
   print(A)
    print(determiniser(A))'''
    rendre_complet(A)


if __name__ == '__main__':
    main()
