# coding=utf8

import re
import pandas as pd

def read_file(filepath):
	res = []
	with open(filepath) as file:
		lines = file.readlines()
		for line in lines:
			s = line.strip("\n")
			s = re.sub("\(.*\)", '', s)
			res.append(s)
	return res

def query(ls_985, ls_211, ls_first_class_uni, ls_first_class_sub, inp):
	res1 = []
	res2 = []
	for s in inp:
		if s in ls_985:
			res1.append("985 211")
		elif s in ls_211:
			res1.append("211")
		else:
			res1.append("")

		if s in ls_first_class_uni:
			res2.append(" 双一流大学")
		elif s in ls_first_class_sub:
			res2.append(" 双一流学科")
		else:
			res2.append("")
	res = [item1 + item2 for item1,item2 in zip(res1,res2)] 
	return res

if __name__ == "__main__":
	list_985 = read_file("./data/985.txt")
	list_211 = read_file("./data/211.txt")
	list_first_class_uni = read_file("./data/双一流大学.txt")
	list_first_class_sub = read_file("./data/双一流学科.txt")

	query_list = ["上海交通大学","上海财经大学","复旦大学" , "中国社科院大学"]

	res = query(list_985, list_211, list_first_class_uni, list_first_class_sub, query_list)
	print(res)