from hmmlearn.hmm import GaussianHMM
import datetime
import numpy as np
import warnings


def interval(date_list):
	result = list()
	for i in range(1, len(date_list)):
		result.append([(date_list[i] - date_list[i - 1]).days])
	return result


X = list()
lengths = list()
user_id_list = list()
with open("sorted.txt", 'r') as file:
	for line in file:
		user_id_list.append(line)
		length = int(file.readline())
		review_time = list()
		for i in range(length):
			info = file.readline().split('\t')
			review_time.append(datetime.datetime(int(info[3][:4]), int(info[3][5:7]), int(info[3][8:10])))
		X.append(interval(review_time))
		lengths.append(length - 1)
		file.readline()
X = np.concatenate(X)

warnings.filterwarnings("ignore")
model = GaussianHMM(n_components=20, n_iter=10000, tol=1, verbose=True)
model.fit(X, lengths)
if model.monitor_.converged:
	print(model.transmat_)
	print(model.means_)
	print(model.covars_)
hidden_state = model.predict(X, lengths)

start = 0
with open("hidden_states.txt", 'w') as file:
	for i in range(len(user_id_list)):
		file.write(user_id_list[i])
		for j in range(lengths[i]):
			file.write(str(hidden_state[start + j]) + '\t')
		start += lengths[i]
		file.write('\n\n')
