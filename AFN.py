mot_vide = "ε"


class Transition():
	def __init__(self, etiquette, destination) -> None:
		self.etiquette = etiquette
		self.etat_dest = destination

	def __str__(self) -> str:
		return f'{self.etiquette} ---> {self.etat_dest}'
	
	def is_epsilon(self):
		return self.etiquette == mot_vide


class Etat():
	def __init__(self, nom, l=None):
		self.nom = nom
		if l == None:
			self.transitions = []
		else:
			self.transitions = l

	def __str__(self) -> str:
		s = ''
		for t in self.transitions:
			s += f'{self.nom} --- {t.__str__()}\n'
		return s

	def __repr__(self) -> str:
		s = ''
		for t in self.transitions:
			s += f'{self.nom} --- {t.__str__()}\n'
		return s

	def add_transition(self, etiquette, etat_dest):
		self.transitions.append(Transition(etiquette, etat_dest))

	def __getitem__(self, key):
		b = []
		for transition in self.transitions:
			if transition.etiquette == key:
				b.append(transition.etat_dest)    
		return b

class Automate():
	def __init__(self, alphabet, initial, etats, final, transitions) -> None:
		self.alphabet = set(alphabet)
		self.etats = {}
		self.etats_init = initial
		self.etats_final = final
		
		for nom_etat in etats:
			self.add_etat(nom_etat)
		for transition in transitions:
			self.etats[transition[0]].add_transition(transition[1], transition[2])
		
	def add_etat(self, nom):
		if not (nom in self.etats): 
			self.etats[nom] = Etat(nom)

	def __str__(self) -> str:
		s = ''
		for etat in self.etats:
			s += self.etats[etat].__str__()
		return s
		
def main():
   alpha="ab"
   etats=[0,1]
   transitions=[(0,'a',1), (0,'b',0), (1,'a',0), (1,'b',1)]
   init = 0
   final = [0]
   A = Automate(alpha, init, etats,final, transitions)
   print(A)


if __name__ == '__main__':
	main()
	