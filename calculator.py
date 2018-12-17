import getopt, sys, csv
from configparser import ConfigParser
from datetime import datetime

class Args(object):
	"""docstring for Args"""
	def __init__(self):
		super(Args, self).__init__()
		self.args = sys.argv[1:]
		self.opts, self.otherArg = getopt.getopt(self.args, "C:c:d:o:")
		print(self.opts)
		self.getConfigFilePath()
		self.getUserDataPath()
		self.getTargetFilePath()
		self.getCity()

	def getCity(self):
		try:
			for o, a in self.opts:
				if o in ("-C"):
					self.city = a.upper()

		except:
			print("city error")

	def getConfigFilePath(self):
		try:
			for o, a in self.opts:
				if o in ("-c"):
					self.configFilePath = a

		except:
			print("config file path not exist")

	def getUserDataPath(self):
		try:
			for o, a in self.opts:
				if o in ("-d"):
					self.userDataPath = a
		except:
			print("user data file path not exist")

	def getTargetFilePath(self):
		try:
			for o, a in self.opts:
				if o in ("-o"):
					self.targetFilePath = a
		except:
			print("target file path not exist")


class Config(object):
	"""docstring for Config"""
	def __init__(self, path, city):
		super(Config, self).__init__()
		self._city = city
		self.config = self._read_config(path)


	def  _read_config(self, path):
		config = ConfigParser()
		config.read(path, encoding="UTF-8")
		itemList = config.items(self._city)
		configObj = {}
		try:
			for line in itemList:
				configObj[line[0].strip()] = line[1].strip()
		except:
			print("config data error")
		print("config data", configObj)
		return configObj


class UserData(object):

	def __init__(self, path):
		self.userdata = self._read_users_data(path)

	def _read_users_data(self,path):
		userdata = {}
		with open(path, 'r') as f:
			userdata = dict(csv.reader(f))
			print(userdata)
		return userdata

		
class IncomeTaxCalculator(object):
	"""docstring for IncomeTaxCalculator"""
	def __init__(self, data, path, config):
		self._config = config
		result = self._getAllData(data)
		self.export(result, path)


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
			eachLine.append(datetime.now())
			result.append(eachLine)
		return result

	def export(self, result, path):
		with open(path, 'w') as f:
			writer = csv.writer(f)
			writer.writerows(result)
	
	def getFee(self, salary):
		try:
			config = self._config
			jishul = float(config.get('JiShuL'.lower()))
			jishuh = float(config.get('JiShuH'.lower()))
			yanglao = float(config.get('YangLao'.lower()))
			yiliao = float(config.get('YiLiao'.lower()))
			shiye = float(config.get('ShiYe'.lower()))
			gongjijin = float(config.get('GongJiJin'.lower()))
			gongshang = float(config.get('GongShang'.lower()))
			shengyu = float(config.get('ShengYu'.lower()))
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

if __name__ == '__main__':
	currentPath = Args()

	configData = Config(currentPath.configFilePath, currentPath.city)

	user = UserData(currentPath.userDataPath)
		
	IncomeTaxCalculator(user.userdata, currentPath.targetFilePath, configData.config)