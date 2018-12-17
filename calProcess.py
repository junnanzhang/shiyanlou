import sys
import csv
from multiprocessing import Process, Queue

class Args(object):
	"""docstring for Args"""
	def __init__(self):
		super(Args, self).__init__()
		self.args = sys.argv[1:]

		self.getConfigFilePath()
		self.getUserDataPath()
		self.getTargetFilePath()

	def getConfigFilePath(self):
		try:
			cIndex = self.args.index('-c')
			self.configFilePath = self.args[cIndex + 1]
		except:
			print("config file path not exist")

	def getUserDataPath(self):
		try:
			dIndex = self.args.index('-d')
			self.userDataPath = self.args[dIndex + 1]
		except:
			print("user data file path not exist")

	def getTargetFilePath(self):
		try:
			oIndex = self.args.index('-o')
			self.targetFilePath = self.args[oIndex + 1]
		except:
			print("target file path not exist")


class Config(object):
	"""docstring for Config"""
	def __init__(self, path):
		super(Config, self).__init__()
		self.config = self._read_config(path)

	def  _read_config(self, path):
		config = {}
		with open(path) as file:
			try:
				for line in file:
					eachLine = line.strip().split('=')
					config[eachLine[0].strip()] = eachLine[1].strip()
			except:
				print("config data error")
		return config


class UserData(Process):

	def __init__(self, path, q1):
		super().__init__()
		self.userdata = self._read_users_data(path)
		self.q1 = q1

	def run(self):
		print("in run ")
		self.q1.put(self.userdata)

	def _read_users_data(self,path):
		userdata = {}
		with open(path, 'r') as f:
			userdata = dict(csv.reader(f))

		return userdata

		
class IncomeTaxCalculator(Process):
	"""docstring for IncomeTaxCalculator"""
	def __init__(self, config, q1, q2):
		super().__init__()
		self._config = config
		self.q1 = q1
		self.q2 = q2

	def run(self):
		data = self.q1.get()
		print(data)
		result = self._getAllData(data)
		self.q2.put(result)


	def _getAllData(self, data):
		result = []
		for key, value in data.items():
			floatValue = float(value)
			eachLine = [key, value]
			feeMoney = self.getFee(floatValue)
			eachLine.append(feeMoney)
			taxMoney = self.getTaxMoney(floatValue, float(feeMoney))
			tax = self.getTax(taxMoney)
			eachLine.append(format(tax, '.2f'))
			resultMoney = floatValue - float(tax) - float(feeMoney)
			eachLine.append(format(resultMoney, '.2f'))
			result.append(eachLine)
		return result
	
	def getFee(self, salary):
		try:
			config = self._config
			jishul = float(config.get('JiShuL'))
			jishuh = float(config.get('JiShuH'))
			yanglao = float(config.get('YangLao'))
			yiliao = float(config.get('YiLiao'))
			shiye = float(config.get('ShiYe'))
			gongjijin = float(config.get('GongJiJin'))
			gongshang = float(config.get('GongShang'))
			shengyu = float(config.get('ShengYu'))
			if salary < jishul:
				salary = jishul
			elif salary > jishuh:
				salary = jishuh
			feePercent = yanglao + yiliao + shiye + gongshang + gongjijin + shengyu
		except:
			print("config data key not exist")
		return format(salary*feePercent, '.2f')

	def getTax(self, taxMoney):
		if  taxMoney > 0 and taxMoney <= 1500:
			return taxMoney * 0.03
		elif  taxMoney > 1500 and taxMoney <= 4500:
			return taxMoney * 0.1 - 105
		elif  taxMoney > 4500 and taxMoney <= 9000:
			return taxMoney * 0.2 - 555
		elif  taxMoney > 9000 and taxMoney <= 35000:
			return taxMoney * 0.25 - 1005
		elif  taxMoney > 35000 and taxMoney <= 55000:
			return taxMoney * 0.3 - 2755
		elif  taxMoney > 55000 and taxMoney <= 80000:
			return taxMoney * 0.35 - 5505
		elif  taxMoney > 80000:
			return taxMoney * 0.45 - 13505
		else:
			return 0.00	

	def getTaxMoney(self, salary, feeMoney):
		taxMoney = salary-feeMoney-3500
		if taxMoney > 0:
			return taxMoney
		else:
			return 0

class ExportData(Process):
	def __init__(self, path, q2):
		super().__init__()
		self.path = path
		self.q2 = q2

	def run(self):
		result = self.q2.get()
		self.export(result, self.path)

	def export(self, result, path):
		with open(path, 'w') as f:
			writer = csv.writer(f)
			writer.writerows(result)

if __name__ == '__main__':

	currentPath = Args()
	q1 = Queue()
	q2 = Queue()
	# print(currentPath.configFilePath, currentPath.targetFilePath, currentPath.userDataPath);
	cfg = Config(currentPath.configFilePath)

	user = UserData(currentPath.userDataPath, q1)

	income = IncomeTaxCalculator(cfg.config, q1, q2)

	export = ExportData(currentPath.targetFilePath, q2)

	user.start()
	income.start()
	export.start()

	user.join()
	income.join()
	export.join()