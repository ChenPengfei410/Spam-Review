import datetime
import operator


person_dict = dict()
with open("../metadata", 'r') as file:
	for line in file:
		line = line.split('\t')
		user_id = line[0]
		user_info = dict()
		user_info["prod_id"] = int(line[1])
		user_info["rating"] = int(float(line[2]))
		user_info["label"] = int(line[3])
		user_info["date"] = datetime.datetime(int(line[4][:4]), int(line[4][5:7]), int(line[4][8:10]))
		if person_dict.__contains__(user_id):
			person_dict[user_id].append(user_info)
		else:
			person_dict[user_id] = list()

for user_id in person_dict.keys():
	person_dict[user_id] = sorted(person_dict[user_id], key=operator.itemgetter('date'))

threshold = 10
record_counter = reviewer_counter = 0
with open("sorted.txt", 'w') as file:
	for user_id in person_dict.keys():
		length = len(person_dict[user_id])
		if length < threshold:
			continue
		record_counter += length
		reviewer_counter += 1
		file.write(user_id + '\n' + str(length) + '\n')
		for info in person_dict[user_id]:
			file.write(str(info["prod_id"]) + '\t' + str(info["rating"]) + '\t' + str(info["label"]) + '\t' +
					   info["date"].strftime("%Y-%m-%d") + '\n')
		file.write('\n')
print(record_counter, reviewer_counter)
