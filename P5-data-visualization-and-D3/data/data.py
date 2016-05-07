from pandas import *
import datetime

data = pandas.read_csv('prosperLoanData.csv')
print data.LoanOriginationDate.describe()
print data.LoanOriginalAmount.describe()

data['year'] = data['LoanOriginationDate'].apply(lambda x: x[:4])
df = data[['BorrowerState', 'year', 'LoanOriginalAmount']].groupby(['BorrowerState','year']).sum()
df.unstack(1).to_csv('loan_amounts.csv', index=True)
