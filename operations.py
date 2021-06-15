import copy
import time
from AF import *


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
    B = copy.deepcopy(A)
    if A.est_deterministe():
        if not B.est_complet():
            B.add_etat("puit")
            for symbol in A.alphabet:
                B["puit"].add_transition(symbol, "puit")
            for etat in B.etats:
                for symbol in A.alphabet:
                    if B[etat][symbol] == None:
                        B[etat].add_transition(symbol, 'puit')
        return B


def main():
    alpha = "ab"
    etats = [1, 2, 3, 4]
    transitions = [(1, 'a', 2), (1, 'a', 3), (3, 'a', 3), (3, 'b', 4), (2, 'a', 4),
                   (4, 'b', 2), ]
    init = [1]
    final = [4]
    A = Automate(alpha, init, etats, final, transitions)
    '''print(A[0])
   print(A.est_deterministe())
   print(A)
   B = copy.deepcopy(A)
   A.add_etat(3)
   print(B)
   print(A)'''
    print(determiniser(A))


if __name__ == '__main__':
    main()
