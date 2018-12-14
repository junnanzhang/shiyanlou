import sys
def getFee(salary):
	return salary*0.165

def getTaxMoney(salary, feeMoney):
	taxMoney = salary-feeMoney-3500
	if taxMoney > 0:
		return taxMoney
	else:
		return 0

def getTax(taxMoney):
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


if __name__ == '__main__':
	list = sys.argv[1:]
	dict = {}
	try:
		for arg in list:
			item = arg.split(':')
			dict[item[0]] = float(item[1])

		for key, value in dict.items():
			feeMoney = getFee(value)
			taxMoney = getTaxMoney(value, feeMoney)

			resultMoney = value - getTax(taxMoney) -feeMoney
			print(key+":"+format(resultMoney, '.2f'))
	# try:

	except:
		print("Parameter Error ")