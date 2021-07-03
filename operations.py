import copy
import time
from typing import final
from collections import deque
from AF import *
from string import ascii_lowercase


def supp_epsi_transition(A):
    '''
        Permet de supprimer les epsilons transitions suivant le principe vu en cours:
        Pour chaque etat, construire son epsilon fermeture, puis déterminer l'image par chaque lettre de l'alphabet par cet ensemble(epsilon fermeture puis relié) on crée donc une transition entre ce sommet et chaque element de l'image étiqueté par ce symbole
    '''
    A1 = Automate(A.alphabet, A.etats_init, A.etats, A.etats_final)
    for etat in A.etats:
        ferm = A.epsilon_fermeture(etat)
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

    if not B.est_deterministe():
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
            B = Automate(
                B.alphabet, [str(set(B.etats_init))], etat, final, transitions)
    return B


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


def minimiser(A):
    '''
        Permet de minimiser un automate tel que décris dans le cours:
        Déjà, s'il n'est pas déterministe, le rendre déterministe
        Ensuite, construire les classes d'équivalences :
            on commmence avec 2 classes {etat finaux}, {etat non finaux}
            on se rassure que pour chaque symbole, l'image de la classe par celui-ci donne une seule classe , si tel n'est pas le cas, diviser cette classe en regroupant les états allant dans la même classe et recommencer
    '''

    # retourne l'index de la classe d'équivalence d'un certaint 'etat'
    def vers_quel_ensemble(list_ensemble, etat) -> int:
        i, n = 0, len(list_ensemble)
        while i < n:
            if etat in list_ensemble[i]:
                return i
            else:
                i += 1

    if not A.est_deterministe():
        A = determiniser(A)
    etat_non_finaux = set([x for x in A.etats if x not in A.etats_final])
    classes_equivalences = list([etat_non_finaux, set(A.etats_final)])
    i = 0
    while i < len(classes_equivalences):
        for symbole in A.alphabet:
            l = []
            for etat in classes_equivalences[i]:
                dest = A[etat][symbole]
                l.append(vers_quel_ensemble(classes_equivalences, dest))
            if len(set(l)) == 1:
                continue
            else:
                ensemble_a_separer = classes_equivalences.pop(i)
                d = {k: [] for k in l}
                for etat, num in zip(ensemble_a_separer, l):
                    d[num].append(etat)
                for key in d:
                    classes_equivalences.append(set(d[key]))
                i = 0
        i += 1
    initial = [str(classe)
               for classe in classes_equivalences if A.etats_init[0] in classe]
    etats = [str(classe) for classe in classes_equivalences]
    final = [
        str(classe) for classe in classes_equivalences if classe.intersection(A.etats_final) != set()
    ]
    transitions = []
    for classe in classes_equivalences:
        for symbole in A.alphabet:
            representant = next(iter(classe))
            i = vers_quel_ensemble(classes_equivalences,
                                   A[representant][symbole])
            if i != None:
                dest = classes_equivalences[i]
                transitions.append((str(classe), symbole, str(dest)))
    return Automate(A.alphabet, initial, etats, final, transitions)


def canonique(A):
    """
        Renvois un automate minimal complet.
    """
    B = minimiser(A)
    if not B.est_complet():
        B = rendre_complet(B)
    return B


def complementaire(A):
    '''
        contruire le complementaire d'un automate tel que vu en cours:
        Déjà s'il n'est pas complet, le rendre complet.
        Ensuite, construire un automate identique à A mais ayant pour états final les états non finaux de A
    '''
    if not A.est_complet():
        A = rendre_complet(A)
    final = set(A.etats.keys()).difference(A.etats_final)
    B = Automate(A.alphabet, initial=A.etats_init, final=final)
    B.copie_etat(A)
    return B


def concatenation(A, B):
    '''
        concatener 2 automates tel que vu en cours :
        Pour nous faciliter les choses, nous déterminisons A et B s'ils sont non déterministes
        L'automate resultat contient tous les états exceptés les états initiaux de B.
        l'état initial est l'état initial de A
        les transitions sont celles de A, celles de B où l'origine n'est pas un de ses états initials, (Final(A),e,sigma(initial de B))
    '''
    if not A.est_deterministe():
        A = determiniser(A)
    if not B.est_deterministe():
        B = determiniser(B)

    if set(A.get_etats()).intersection(B.get_etats()) != set():
        return "Veuillez entrez 2 automates ayant des états différents"
    etats = set(A.get_etats() + B.get_etats()).difference(B.etats_init)
    finals = []
    if set(B.etats_init).intersection(B.etats_final) == set():
        finals = B.etats_final
    else:
        finals = set(B.etats_final + A.etats_final).difference(B.etats_init)
    C = Automate(A.alphabet, etats=etats, initial=A.etats_init, final=finals)
    C.copie_etat(A)
    transitions_2 = B.get_transitions()
    for transition in transitions_2:
        if not (transition[0] in B.etats_init):
            C.add_transition(transition[0], transition[1], transition[2])
        else:
            for etat in A.etats_final:
                C.add_transition(etat, transition[1], transition[2])
    return C


def miroir(A):
    """
        changer le sens des transitions de l'automate A, les états finaux deviennent initiaux et vice verca.
        Après cette transformation,  si l'automate resultant n'est déterministe, le déterminiser le le retourner

    """
    transitions = A.get_transitions()
    transitions_miroir = []
    for transition in transitions:
        transitions_miroir.append(
            (transition[2], transition[1], transition[0]))
    C = Automate(A.alphabet, A.etats_final, A.get_etats(),
                 A.etats_init, transitions_miroir)
    if not C.est_deterministe():
        C = determiniser(C)
    return C


def iterer(A):
    """
        Relier tout état final à un état initial par une epsilon transition
        déterminiser
    """
    reconnait_epsi = determiniser(A).reconnait(mot_vide)
    B = copy.deepcopy(A)
    for etat in B.etats_final:
        for init in B.etats_init:
            B.add_transition(etat, mot_vide, init)
            if not reconnait_epsi:
                B.add_transition(init, mot_vide, etat)
    if not B.est_deterministe():
        B = determiniser(B)
    return B


def transform_post_fixe(expression):
    caractere_accepte = ascii_lowercase + '0123456789'
    file = deque()
    pile = list()
    for i in range(len(expression)):
        if expression[i] in caractere_accepte:
            file.append(expression[i])
            if i > 0 and expression[i-1] in ')*' + caractere_accepte:
                file.append('.')
        elif expression[i] == '(':
            if i > 0 and expression[i-1] in ')' + caractere_accepte:
                pile.append('.')
            pile.append(expression[i])

        elif expression[i] == ')':
            a = len(pile)
            while a > 0 and pile[a - 1] != '(':
                file.append(pile.pop())
                a -= 1
            pile.pop()
            if a < 0:
                return "expression invalide"
        else:
            if expression[i] == '+':
                a = len(pile)-1
                while a >= 0 and pile[a] in '*.':
                    file.append(pile.pop())
                    a -= 1
            if expression[i] == '*':
                file.append('*')
            else:
                pile.append(expression[i])

    a = len(pile) - 1
    while len(pile) != 0:
        if pile[a] == '(':
            return "expression invalide"
        else:
            file.append(pile.pop())
            a -= 1
    return ''.join(file)


def construction_thompson(expression):
    '''
        construction de thompson: nous prenons en entré une expression en notation post fixé, et construisons l'automate thompson pur par ajout de transitions dans une liste de transition 
        nous avons un tableau de tuple a 2 dimension : son rôle est de pouvoir faire les liaisons entre nous constructions précédente et l'opérateur qu'on rencontre
    '''
    alphabet = []
    caractere_accepte = ascii_lowercase + '0123456789'
    transitions, av_dernier = list(), list()
    num_init, num_final, nb_etat = -1, 0, 0
    for i in range(len(expression)):
        if expression[i] in caractere_accepte:
            alphabet.append(expression[i])
            nb_etat += 1
            av_dernier.append((num_init, num_final))
            transitions.append((num_init, expression[i], num_final))
            num_init, num_final = num_init - 1, num_final + 1
        else:
            if expression[i] == '+':
                nb_etat += 1
                p = av_dernier.pop()
                q = av_dernier.pop()
                transitions.append((num_init, mot_vide, p[0]))
                transitions.append((num_init, mot_vide, q[0]))
                transitions.append((p[1], mot_vide, num_final))
                transitions.append((q[1], mot_vide, num_final))
                av_dernier.append((num_init, num_final))

                num_init, num_final = num_init - 1, num_final + 1

            elif expression[i] == '*':
                nb_etat += 1
                p = av_dernier.pop()
                transitions.append((p[1], mot_vide, p[0]))
                transitions.append((p[1], mot_vide, num_final))
                transitions.append((num_init, mot_vide, p[0]))
                transitions.append((num_init, mot_vide, num_final))
                av_dernier.append((num_init, num_final))

                num_init, num_final = num_init - 1, num_final + 1

            elif expression[i] == '.':
                p = av_dernier.pop()
                q = av_dernier.pop()
                transitions.append((q[1], mot_vide, p[0]))
                av_dernier.append((q[0], p[1]))

    etats = []
    for i in range(0 - nb_etat, nb_etat):
        etats.append(i)
    return Automate(alphabet, [av_dernier[0][0]], etats, [av_dernier[0][1]], transitions)


def construction_glushkov(expression):
    pass


def supprimer_etat(etat, transitions):
    transitions_origine = []
    boucle = []
    transitions_destination = []
    i = 0
    while i < len(transitions):
        if transitions[i][0] == etat and transitions[i][0] != transitions[i][2]:
            transitions_origine.append(transitions.pop(i))
        elif transitions[i][2] == etat and transitions[i][0] != transitions[i][2]:
            transitions_destination.append(transitions.pop(i))
        elif transitions[i][0] == etat and transitions[i][0] == transitions[i][2]:
            boucle.append(transitions.pop(i))
        else:
            i += 1

    eti_boucle = ''
    for i in range(len(boucle)):
        eti_boucle += boucle[i][1]
        if i != len(boucle) - 1:
            eti_boucle += '+'
    for t in transitions_destination:
        for t2 in transitions_origine:
            etiquette = ''
            if t[1] == mot_vide and t2[1] == mot_vide:
                if eti_boucle not in [mot_vide, '']:
                    etiquette += f'({eti_boucle})*'
                else:
                    etiquette = mot_vide
            elif t[1] == mot_vide and t2[1] != mot_vide:
                if eti_boucle not in [mot_vide, '']:
                    etiquette += f'({eti_boucle})*'
                etiquette += t2[1]
            elif t[1] != mot_vide and t2[1] == mot_vide:
                etiquette = t[1]
                if eti_boucle not in [mot_vide, '']:
                    etiquette += f'({eti_boucle})*'
            else:
                etiquette = t[1]
                if eti_boucle not in [mot_vide, '']:
                    etiquette += f'({eti_boucle})*'
                etiquette += t2[1]
            transitions.append((t[0], etiquette, t2[2]))


def automate_vers_expression(A):
    transitions = A.get_transitions()
    etat_nbre_transition = {etat: 0 for etat in A.etats}
    for t in transitions:
        if t[0] == t[2]:
            etat_nbre_transition[t[0]] += 1
        else:
            etat_nbre_transition[t[0]] += 1
            etat_nbre_transition[t[2]] += 1
    l = sorted(etat_nbre_transition.items(), key=lambda item: item[1])
    etat_nbre_transition = []
    i = 1
    j = 0
    etat_nbre_transition.append(l[0])
    while i < len(l):
        if etat_nbre_transition[j][1] < l[i][1]:
            etat_nbre_transition.append(l[i])
        else:
            k = j
            while k >= 0 and etat_nbre_transition[k][1] == l[i][1] and etat_nbre_transition[k][0] < l[i][0]:
                k -= 1
            etat_nbre_transition.insert(k+1, l[i])
        i += 1
        j += 1

    for e in A.etats_init:
        transitions.append(('Init', mot_vide, e))
    for e in A.etats_final:
        transitions.append((e, mot_vide, 'Final'))

    for etat in etat_nbre_transition:
        supprimer_etat(etat[0], transitions)

    expression = transitions[0][1]
    for i in range(1, len(transitions)):
        expression += f' + {transitions[i][1]}'

    return expression


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

    alpha3 = "abc"
    etats3 = [0, 1, 2, 3, 4, 5]
    transitions3 = [
        (0, 'a', 2), (0, 'b', 0), (0, 'c', 1), (1, 'a', 3), (1, 'b', 1),
        (1, 'c', 3), (2, 'a', 2), (2, 'b', 4), (2, 'c', 3), (3, 'a', 3),
        (3, 'b', 5), (3, 'c', 3), (4, 'a', 4), (4, 'b', 4),
        (4, 'c', 5), (5, 'a', 5), (5, 'b', 5), (5, 'c', 5),
    ]

    init3 = [0]
    final3 = [4, 5]
    A3 = Automate(alpha3, init3, etats3, final3, transitions3)

    alpha4 = [0, 1]
    etats4 = ['a', 'b', 'c', 'd', 'e', 'f']
    transitions4 = [
        ('a', 0, 'b'), ('a', 1, 'c'), ('b', 0, 'a'), ('b', 1, 'd'),
        ('c', 0, 'e'), ('c', 1, 'f'), ('d', 0, 'e'), ('d', 1, 'f'),
        ('e', 0, 'e'), ('e', 1, 'f'), ('f', 0, 'f'), ('f', 1, 'f'),
    ]

    init4 = ['a']
    final4 = ['d', 'c', 'e']
    A4 = Automate(alpha4, init4, etats4, final4, transitions4)

    alpha5 = ['a', 'b']
    etats5 = [0, 1, 2, 3]
    transitions5 = [
        (0, 'a', 1), (0, mot_vide, 2), (1, 'a', 0), (1, 'b', 1), (2, 'a', 3), (2, 'b', 1), (3, mot_vide, 0)]

    init5 = [0]
    final5 = [2]
    A5 = Automate(alpha5, init5, etats5, final5, transitions5)

    alpha6 = ['a', 'b', 'c']
    etats6 = [1, 2, 3, 4, 5, 6]
    transitions6 = [
        (1, 'a', 2), (1, 'b', 4), (2, 'a', 5), (2, 'b', 3), (2, 'c', 2),
        (3, 'a', 6), (3, 'b', 4), (4, 'c', 5), (5, 'a', 5), (5, 'a', 6),
    ]

    init6 = [1]
    final6 = [6]
    A6 = Automate(alpha6, init6, etats6, final6, transitions6)

    alpha7 = ['a', 'b']
    etats7 = ['A', 'B', 'C', 'D', 'E']
    transitions7 = [
        ('A', 'a', 'B'), ('A', 'b', 'C'), ('B', 'a', 'B'), ('B', 'b', 'D'),
        ('C', 'a', 'B'), ('C', 'b', 'C'), ('D', 'a', 'B'), ('D', 'b', 'E'),
        ('E', 'a', 'B'), ('E', 'b', 'C')
    ]

    init7 = ['A']
    final7 = ['E']
    A7 = Automate(alpha7, init7, etats7, final7, transitions7)

    alpha3 = "ab"
    etats3 = [0, 1, 2, ]
    transitions3 = [
        (0, 'a', 1), (0, 'b', 1), (1, 'a', 0), (1, 'b', 2), (2, 'b', 0)
    ]

    init3 = [0]
    final3 = [0]
    A3 = Automate(alpha3, init3, etats3, final3, transitions3)
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
    mot = "aaba"
    print(intersection(A1, A2))print(A1.reconnait(mot))
    print(complementaire(A1).reconnait(mot))
    print(minimiser(A4))
    print(A1.reconnait("abaaa"))
    print(miroir(A1).reconnait("aaaba"))
    print(iterer(A1))
    print(determiniser(A5))
    print(concatenation(A6, A7))
    es = 'ab(a+b)*+c+d+(a*b)*'
    e = transform_post_fixe(es)
    print(es, e)
    if e != 'expression invalide':
        B = construction_thompson(e)
        print(B)
        # time.sleep(3)
        B = canonique(B)
        print(B)
        print(B.reconnait(''))
    else:
        print("synthaxe invalide")
    
    print(automate_vers_expression(A2))
    '''


if __name__ == '__main__':
    main()
