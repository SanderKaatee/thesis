import pandas as pd
from scipy.stats import ttest_ind

data = pd.read_csv('refactored_result_first.csv')

t_statistic, p_value = ttest_ind(data['AABL_correct'], data['refactored_correct'])

print("t-statistic:", t_statistic)
print("p-value:", p_value)


