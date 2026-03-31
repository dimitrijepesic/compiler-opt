from abc import ABC, abstractmethod
import json
import os
from datetime import datetime

class OptimizerAgent(ABC):

	"""
	Abstraktna bazna klasa gde će stati svi modeli. Ovo je način da svaki
	agent ima isti interfejs.
	"""

	def __init__(self, env, log_dir="results/"):
		self.env = env
		self.log_dir = log_dir
		self.history = [] # Ovde čuvam tok treninga
		self.best_sequence = []
		self.best_score = float('inf')

		if not os.path.exists(log_dir):
			os.makedirs(log_dir)

	@abstractmethod
	def train(self, *args, **kwargs):

		"""
		Ovu funkciju svaki agent implementira ponaosob.
		"""
		pass

	def update_best(self, score, actions):

		"""
		Čuvanje rekorda.
		"""
		if score<self.best_score:
			self.best_score = score
			self.best_sequence = list(actions)
			return True
		return False

	def save_results(self, filename = None):

		"""
		Univerzalna logika za čuvanje rezultata u json fajl.
		"""

		if filename is None:
			timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
			agent_name = self.__class__.__name__
			bench_name = str(self.env.benchmark).split("/")[-1] if self.env.benchmark else "unknown"
			filename = f"{agent_name}_{bench_name}_{timestamp}.json"
		filepath = os.path.join(self.log_dir,filename)

		data = {
			"agent":self.__class__.__name__,
			"benchmark":str(self.env.benchmark),
			"timestamp":datetime.now().isoformat(),
			"best_score":self.best_score,
			"best_sequence":self.best_sequence,
			"history_length":len(self.history),
			"history": self.history
		}

		try:
			with open(filepath,"w") as f:
				json.dump(data,f,indent = 2)
			print(f"\n[SISTEM] Rezultati sacuvani u: {filepath}")
		except Exception as e:

			print(f"[GRESKA] Nije uspelo cuvanje rez:  {e}")
