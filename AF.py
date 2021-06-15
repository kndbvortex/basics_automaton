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
            self.etats[transition[0]].add_transition(
                transition[1], transition[2])
            if transition[1] == mot_vide:
                self.spontanee = True

    # Ajoute un état dans l'automate
    def add_etat(self, nom):
        if not (nom in self.etats):
            self.etats[nom] = Etat(nom)

    # vérifie qu'un mot appartient à un langage
    def reconnait(self, mot) -> bool:
        q = self.etats_init[0]
        i = 0
        n = len(mot)
        while i < n:
            q = self.etats[q][mot[i]]
            i += 1
            if q == [] or q == None:
                return False
        for etat in self.etats_final:
            if etat == q:
                return True
        return False

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

    def epsilon_fermeture(self, etat, b):
        q = self[etat]
        fermeture = set()
        for transition in q.transitions:
            if transition.is_epsilon():
                fermeture.add(transition.etat_dest)
        a = set(fermeture) - {b, etat}
        for e in a:
            fermeture.update(self.epsilon_fermeture(e, b))
        fermeture.add(etat)
        return fermeture

    def __str__(self) -> str:
        s = ''
        for etat in self.etats:
            s += self.etats[etat].__str__()
        return s

    # surcharge de l'opérateur d'indexage afin de pouvoir obtenir l'etat de nom 'key'
    def __getitem__(self, key):
        return self.etats[key]
