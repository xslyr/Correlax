#/usr/bin/python3
#!encoding:utf8
#
#	Created at 26-05-2023
#	Coder: Wesley R. Silva
#	Library functionality extension of correlation matrix pandas.corr()
#

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


# class to encoder column by order of their occurrence
class LbEncoder(LabelEncoder):
	def __init__(self):
		super().__init__()
		self.labels = []

	def get_unique(self, data):
		if isinstance(data, pd.Series): return data.unique()
		elif isinstance(data, np.ndarray) or isinstance(data, list): return np.unique(data)
		else: raise ValueError("The parameter isn't of knowed type")

	def get_current_sort(self,data):
		current_sort =[]
		for i in data:
			if i not in current_sort: current_sort.append(i)
		return current_sort
	
	def fit_by_order(self, data, sort_by=()):
		if not (isinstance(data, np.ndarray) or isinstance(data, pd.Series)):
			raise Exception('The data parameter must be Panda Series or Numpy Array')
		self.data = data.copy()
		super().fit(self.data)
		self.labels = self.classes_
		if isinstance(sort_by, str):
			if sort_by in ['desc','occurrence']:
				self.labels = self.get_current_sort(self.data)
				if sort_by == 'desc':
					self.labels.sort(reverse=True)
		elif isinstance(sort_by, list):
			self.labels = sort_by
		self.classes_ = np.array(self.labels, dtype=object)

	def fit_transform(self, data, sort_by=()):
		if not (isinstance(data, np.ndarray) or isinstance(data, pd.Series)):
			raise Exception('The data parameter must be Panda Series or Numpy Array')
		self.fit_by_order(data, sort_by=sort_by)
		self.data = super().transform(self.data)
		return self.data


class Correlax:
	def __init__(self, data):
		aux = pd.DataFrame(np.zeros(shape=data.shape), columns=data.columns)
		for col in data.columns:
			if data[col].dtype == 'object':
				aux[col] = LbEncoder().fit_transform( data[col] , sort_by='occurrence')
			elif data[col].dtype in ('int64','float64'):
				aux[col] =data[col]
		self.corr = aux.corr()
		
		
	def sort_by(self, column, ascending=False):
		return self.corr.sort_values(column, ascending=ascending)[column]
	
	def print_by(self, column, ascending=False):
		for item in self.corr.index:
			print('{} : {}'.format( item, self.corr[column][item] ))
	
	
	
	
