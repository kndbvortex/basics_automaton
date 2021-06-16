import copy
import time
from AF import *


def supp_epsi_transition(A):
    '''
        Permet de supprimer les epsilons transitions suivant le principe vu en cours:
        Pour chaque etat, construire son epsilon fermeture, puis déterminer l'image par chaque lettre de l'alphabet par cet ensemble(epsilon fermeture puis relié) on crée donc une transition entre ce sommet et chaque element de l'image étiqueté par ce symbole
    '''
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
    S'il est à transition spontanée, supprimer celles-ci
    on commence en construisant un ensemble constitué des états initiaux ,puis à partir de celui-ci, on construis les états de proche en proche par dtermination de la destination de chaque element de l'ensemble en lisant un certain symbole de l'alphabet
    '''
    B = ''
    if A.spontanee:
        B = supp_epsi_transition(A)
    else:
        B = copy.deepcopy(A)

    etats_definitifs = []
    transitions = []
    if not B.est_deterministe():
        initial = set(B.etats_init)
        l = []
        l.append(set(initial))
        while len(l) != 0:
            etat_en_cours = l.pop(0)
            for symbol in B.alphabet:
                initial.clear()
                for e in etat_en_cours:
                    a = B[e][symbol]
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
                    if not initial in etats_definitifs:
                        l.append(set(initial))
            if not etat_en_cours in etats_definitifs:
                etats_definitifs.append(set(etat_en_cours))
        final = [
            str(etat) for etat in etats_definitifs if etat.intersection(B.etats_final) != set()
        ]
        etat = [str(etat) for etat in etats_definitifs]
        return Automate(B.alphabet, [str(set(B.etats_init))], etat, final, transitions)


def rendre_complet(A):
    '''
        Si l'automate n'est pas déterministe, le rendre détermiste ensuite,
        si l'on se rend compte qu'il n'est pas complet alors créer un état puit et relier vers lui toute les transition manquante
    '''
    B = ''
    if not A.est_deterministe():
        B = determiniser(A)
    else:
        B = copy.deepcopy(A)

    if not B.est_complet():
        B.add_etat("puit")
        for symbol in B.alphabet:
            B["puit"].add_transition(symbol, "puit")
        for etat in B.etats:
            for symbol in B.alphabet:
                if B[etat][symbol] == None:
                    B[etat].add_transition(symbol, 'puit')
    return B


def union(A, B):
    '''
        Déjà A et B doivent etre complet et donc s'il ne le sont pas les rendre complet.
        Ensuite, on commence par construire un tuple ayant pour valeur l'etat initial de A et celui de B rendu complet. On construis notre automate de proche en proche par détermination de la destination de chaque element de l'ensemble en lisant un certain symbole de l'alphabet
        les états finaux sont ceux comportant l'état final de A ou celui de B
    '''
    if not A.est_complet():
        A = rendre_complet(A)
    if not B.est_complet():
        B = rendre_complet(B)
    etats_definitifs = []
    transitions = []
    initial = ()
    l = []
    l.append((A.etats_init[0], B.etats_init[0]))
    while len(l) != 0:
        etat_en_cours = l.pop(0)
        for symbol in B.alphabet:
            initial = (A[etat_en_cours[0]][symbol],
                       B[etat_en_cours[1]][symbol])
            t = (str(etat_en_cours),
                 symbol, str(initial))
            if not t in transitions:
                transitions.append(t)
            if not initial in etats_definitifs:
                l.append(initial)
        if not etat_en_cours in etats_definitifs:
            etats_definitifs.append(etat_en_cours)
    final = [
        str(etat) for etat in etats_definitifs if set(etat).intersection(set(B.etats_final + A.etats_final)) != set()
    ]
    etat = [str(etat) for etat in etats_definitifs]
    return Automate(B.alphabet, [str((A.etats_init[0], B.etats_init[0]))], etat, final, transitions)


def intersection(A, B):
    '''
        Déjà A et B doivent etre complet et donc s'il ne le sont pas les rendre complet.
        Ensuite, on commence par construire un tuple ayant pour valeur l'etat initial de A et celui de B rendu complet. On construis notre automate de proche en proche par détermination de la destination de chaque element de l'ensemble en lisant un certain symbole de l'alphabet
        les états finaux sont ceux comportant tous 2 l'état final de A et celui de B
    '''
    if not A.est_complet():
        A = rendre_complet(A)
    if not B.est_complet():
        B = rendre_complet(B)
    etats_definitifs = []
    transitions = []
    initial = ()
    l = []
    l.append((A.etats_init[0], B.etats_init[0]))
    while len(l) != 0:
        etat_en_cours = l.pop(0)
        for symbol in B.alphabet:
            initial = (A[etat_en_cours[0]][symbol],
                       B[etat_en_cours[1]][symbol])
            t = (str(etat_en_cours),
                 symbol, str(initial))
            if not t in transitions:
                transitions.append(t)
            if not initial in etats_definitifs:
                l.append(initial)
        if not etat_en_cours in etats_definitifs:
            etats_definitifs.append(etat_en_cours)
    final = [
        str(etat) for etat in etats_definitifs if set(etat).intersection(set(B.etats_final + A.etats_final)) == set(B.etats_final + A.etats_final)
    ]
    etat = [str(etat) for etat in etats_definitifs]
    return Automate(B.alphabet, [str((A.etats_init[0], B.etats_init[0]))], etat, final, transitions)


def main():
    alpha = "ab"
    etats = [0, 1, 2, 3, 4]
    transitions = [(0, 'a', 1), (0, mot_vide, 2), (1, mot_vide, 4),
                   (2, 'a', 3), (2, 'b', 3), (3, mot_vide, 4), (3, 'b', 2), ]

    init = [0]
    final = [4]
    A = Automate(alpha, init, etats, final, transitions)
    alpha1 = "ab"
    etats1 = [0, 1]
    transitions1 = [(0, 'a', 1), (0, 'b', 0), (1, 'a', 0),
                    (1, 'b', 1), ]

    init1 = [0]
    final1 = [0]
    A1 = Automate(alpha1, init1, etats1, final1, transitions1)

    alpha2 = "ab"
    etats2 = [0, 1]
    transitions2 = [(0, 'a', 0), (0, 'b', 1), (1, 'a', 1),
                    (1, 'b', 0), ]

    init2 = [0]
    final2 = [0]
    A2 = Automate(alpha2, init2, etats2, final2, transitions2)

    '''print(A[0])
    print(A.est_deterministe())
    print(A)
    B = copy.deepcopy(A)
    A.add_etat(3)
    print(B)
    print(A)
    print(determiniser(A))
    print(rendre_complet(A))
    print('\n\n\n')
    print(determiniser(A))
    print(intersection(A1, A2))
    '''


if __name__ == '__main__':
    main()
