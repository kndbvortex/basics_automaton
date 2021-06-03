class Transition():
	def __init__(self, origine, etiquette, destination) -> None:
		self.origine = origine
		self.etiquette = etiquette
		self.etat_dest = destination

	def __str__(self) -> str:
		return f'{self.etiquette}--->{self.etat_dest}'
	
	def is_epsilon(self):
		return self.etiquette == mot_vide

        
class AFN():
	def __init__(self, alpha="ab", etats=[0,1], transitions=[(0,'b',0), (0,'a',1), (1,'a',0), (1,'b',1)], init = 0, final = [0]):
		self.alphabet = set(alpha)
		self.etats = etats
		self.etat_initial = init
		self.etats_finaux = final
		self.transitions = [transition(i,j,k) for i,j,k in transitions]

	def delta(self, q, a):
		for transition in self.transitions:
			if transition.origine == q and transition.etiquette == a:
				return transition.etat_dest
	
	def reconnait(self, mot) -> bool:
		q = self.etat_initial
		i = 0
		n = len(mot)
		while i < n:
			q = self.delta(q, mot[i])
			i += 1
			if q == None:
				return False
		for etat in self.etats_finaux:
			if etat == q:
				return True
		return False