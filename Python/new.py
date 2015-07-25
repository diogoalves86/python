import pwd

class Estudos:
	def diogo(self):
		senha = pwd.getpwnam("lol")
		print(senha)


estudo = Estudos()
estudo.diogo()