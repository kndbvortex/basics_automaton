import copy
import time


mot_vide = "ε"


class Transition():
    ''' Classe représentant partiellement une transition(étiquette et nom de la destination) '''

    def __init__(self, etiquette, destination) -> None:
        self.etiquette = etiquette
        self.etat_dest = destination

    def __str__(self) -> str:
        return f'{self.etiquette} ---> {self.etat_dest}'

    # vérifie si une transition quelconque est spontanée
    def is_epsilon(self):
        return self.etiquette == mot_vide


class Etat():
    '''Représente un etat (Nom et transitions sortantes'''

    def __init__(self, nom, l=None):
        self.nom = nom
        if l == None:
            self.transitions = []
        else:
            self.transitions = list(l)

    def __str__(self) -> str:
        if self.transitions != []:
            s = ''
            for t in self.transitions:
                s += f'{self.nom} --- {t.__str__()}\n'
            return s
        else:
            return f'{self.nom} ---\n'

    def __repr__(self) -> str:
        if self.transitions != []:
            s = ''
            for t in self.transitions:
                s += f'{self.nom} --- {t.__str__()}\n'
            return s
        else:
            return f'{self.nom} ---'

    # ajouter une nouvelle transition sortante à cet état
    def add_transition(self, etiquette, etat_dest):
        self.transitions.append(Transition(etiquette, etat_dest))

    # surcharge de l'opérateur d'indexage afin de pouvoir obtenir le nom des des etats de destination
    # pour les transitions étiquettée par le symbole 'key'
    def __getitem__(self, key):
        b = []
        for transition in self.transitions:
            if transition.etiquette == key:
                b.append(transition.etat_dest)
        n = len(b)
        if n == 1:
            return b[0]
        elif n == 0:
            return None
        else:
            return b


class Automate():
    '''
            Représentation d'un automate:
    Il est caractérisé par un alphabet, un ensemble d'état, ceux finaux et initiaux
    et d'un ensemble de valeur sous la forme d'une liste de tuple (i, j, k)
    avec i l'origine , j l'étiquette, k l'etat de destination
    '''

    def __init__(self, alphabet, initial=[], etats=[], final=[], transitions=[]) -> None:
        self.alphabet = set(alphabet)
        self.etats = {}
        self.etats_init = list(initial)
        self.etats_final = list(final)
        self.spontanee = False

        for nom_etat in etats:
            self.add_etat(nom_etat)
        for transition in transitions:
            self.add_transition(transition[0], transition[1], transition[2])
            if transition[1] == mot_vide:
                self.spontanee = True

    # Ajoute un état dans l'automate
    def add_etat(self, nom):
        if not (nom in self.etats):
            self.etats[nom] = Etat(nom)

    def get_etats(self):
        return [etat for etat in self.etats]

    # Ajouter une transition dans l'automate
    def add_transition(self, origine, etiquette, destination):
        if origine in self.etats:
            if destination in self.etats:
                if etiquette in self.alphabet.union(mot_vide):
                    self[origine].add_transition(etiquette, destination)
                    if etiquette == mot_vide:
                        self.spontanee = True

    def get_transitions(self):
        transitions = []
        for etat in self.etats:
            for transition in self.etats[etat].transitions:
                transitions.append(
                    (etat, transition.etiquette, transition.etat_dest))
        return transitions

    # copie des différents états d'un automates A
    def copie_etat(self, A):
        for k, v in A.etats.items():
            self.add_etat(k)
            self.etats[k] = copy.deepcopy(v)

    # vérifie qu'un mot appartient à un langage
    def reconnait(self, mot) -> bool:
        l = [i for i in self.etats_init]
        for i in range(len(mot)):
            a = list(l)
            l.clear()
            for etat in a:
                epsi = self.epsilon_fermeture(etat)
                for e in epsi:
                    l.append(e)
                dest = self[etat][mot[i]]
                if dest != None:
                    if type(dest) == type([]):
                        for e in dest:
                            l.append(e)
                    else:
                        l.append(dest)
        if len(mot) == 0:
            for e in self.etats_init:
                a = self.epsilon_fermeture(e)
                for t in a:
                    l.append(t)
        if set(l).intersection(self.etats_final) != set():
            return True
        else:
            return False

    # vérifie si un automate est déterministe suivant le principe suivant
    # s'il contient plus d'un etat initial est est ND
    # si parmi les états de l'automate, il y'a un état pour lequel pour un symbole de l'alphabet, on se retrouve sur plus d'un état

    def est_deterministe(self) -> bool:
        if len(self.etats_init) != 1 or self.spontanee:
            return False
        for etat in self.etats:
            for symbole in self.alphabet:
                if type(self.etats[etat][symbole]) == type([]):
                    return False
        return True

    def est_complet(self):
        if self.est_deterministe():
            for etat in self.etats:
                for symbol in self.alphabet:
                    if self.etats[etat][symbol] == None:
                        return False
            return True
        else:
            return False

    # ensemble de tout les etats accessible partant de etat uniquement par des epsilons transitions
    def epsilon_fermeture(self, etat):
        traiter = set()
        en_cours = [etat]
        while len(en_cours) != 0:
            e = en_cours.pop()
            if e not in traiter:
                for transition in self[e].transitions:
                    if transition.is_epsilon():
                        en_cours.append(transition.etat_dest)
            traiter.add(e)
        return traiter

    def __str__(self) -> str:

        s = f'Etat initiaux : {self.etats_init}\nEtat finaux :{self.etats_final}\n'
        for etat in self.etats:
            s += self.etats[etat].__str__()
        return s

    # surcharge de l'opérateur d'indexage afin de pouvoir obtenir l'etat de nom 'key'
    def __getitem__(self, key):
        return self.etats[key]


if __name__ == '__main__':
    alphabet = 'ab'
    etats = [0, 1, 2, 3]
    init = [1]
    final = [0]
    transitions = [
        (1, 'a', 0), (1, 'a', 3), (2, 'b', 0), (2, 'b', 3),
        (3, 'a', 0), (3, 'b', 0), (0, 'a', 1), (0, 'a', 2),
    ]
    A = Automate(alphabet, init, etats, final, transitions)
    print(A.reconnait('aabab'))
