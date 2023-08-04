import pandas as pd
from scipy.stats import ttest_ind

data = pd.read_csv('./exp3/data/result_first.csv')

t_statistic, p_value = ttest_ind(data['pseudocode_correct'], data['AABL_correct'])


df = len(data['AABL_correct']) + len(data['pseudocode_correct']) - 2

print("t-statistic:", t_statistic)
print("p-value:", p_value)
print("degrees of freedom:", df)
