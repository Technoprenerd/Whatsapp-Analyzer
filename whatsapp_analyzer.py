from myimports import *
from create_whatsapp_data import create_whatsapp_data

chat_file = 'whatsapp-chat-FIRSTNAME-LASTNAME.txt'
name_person_1 = ' YOURNAME: '
name_person_2 = ' PERSONNAME: '

person1_file = name_person_1+"_datastore.json"
person2_file = name_person_2+"_datastore.json"

p1_file_exists = os.path.isfile(person1_file)
p2_file_exists = os.path.isfile(person2_file)

if p1_file_exists | p2_file_exists == False:
    print 'No file on disk, making it now...'
    create_whatsapp_data(chat_file, name_person_1, name_person_2)

def create_msg_vs_date(json_file):
	fname = str(json_file)
	json_data = open(fname)
	data = json.load(json_data)

	sorted_message = dict()
	times = list()
	
	for message in data:
		datetime_str = message['Datetime']
		datetime_obj = datetime.strptime(datetime_str,  '%Y-%m-%d %H:%M:%S')

		msg_date = datetime_obj.strftime("%x")
		msg_time = datetime_obj.strftime("%X")
		times.append(msg_time)

		if msg_date not in sorted_message.keys():
			sorted_message[msg_date] = [{'Time': msg_time, 'Message': message['Message']}]
		else:
			sorted_message[msg_date].append({'Time': msg_time, 'Message': message['Message']})

	date_count_msgs = dict()

	#count msgs on day, store in day:int

	for date in sorted_message:
		msgs_on_day = sorted_message[date]
		date_count_msgs[date] = len(msgs_on_day)

	json_data.close()

	return date_count_msgs

person1_date_count, person2_date_count = create_msg_vs_date(person1_file), create_msg_vs_date(person2_file)

def msg_vs_date(person1, person2):
	X1 = np.array([matplotlib.dates.datestr2num(person1.keys())])
	Y1 = np.array([person1.values()])

	X2 = np.array([matplotlib.dates.datestr2num(person2.keys())])
	Y2 = np.array([person2.values()])

	#must have same shape! x.shape = y.shape

	#plot graph	
	plt.xlabel("Date")
	plt.ylabel("Number of Messages")
	plt.title("Date vs number of messages - Person1, Person2")

	p1 = plt.plot_date(X1, Y1, color='red', label="Person1")
	p2 = plt.plot_date(X2, Y2, color='black', label="Person2")

	red_patch = mpatches.Patch(color='red', label="Person1")
	black_patch = mpatches.Patch(color='black', label="Person2")
	plt.legend([red_patch,black_patch], ["Person1", "Person2"])

	plt.show()

def date_vs_time(json_file):
	fname = str(json_file)
	json_data = open(fname)
	data = json.load(json_data)

	sorted_message = dict()
	dt_list = list()
	times = list()
	
	for message in data:
		datetime_str = message['Datetime']
		datetime_obj = datetime.strptime(datetime_str,  '%Y-%m-%d %H:%M:%S')

		msg_date = datetime_obj.strftime("%x")
		msg_time = datetime_obj.strftime("%X")
		times.append(msg_time)
		dt_list.append(datetime_obj)

		if msg_date not in sorted_message.keys():
			sorted_message[msg_date] = [msg_time]
		else:
			sorted_message[msg_date].append([msg_time])

	#Frequency of week days
	week_day = list()
	for i in dt_list:
		day = i.weekday()
		week_day.append(day)

	counter = collections.Counter(week_day)
	most_common_day = counter.most_common(1)[0][0]

	#Average time calculation. Magic:P
	time_list = map(lambda s: int(s[6:8]) + 60*(int(s[3:5]) + 60*int(s[0:2])), times)
	average = sum(time_list)/len(time_list)
	bigmins, secs = divmod(average, 60)
	hours, mins = divmod(bigmins, 60)
	average = str("%02d:%02d:%02d" % (hours, mins, secs))

	x = np.array([matplotlib.dates.datestr2num(sorted_message.keys())])
	y = np.array([matplotlib.dates.datestr2num(times)])
	
	#plot graph	
	fig = plt.figure()
	fig.suptitle('Date vs Time', fontsize=14, fontweight='bold')

	ax = fig.add_subplot(111)
	fig.subplots_adjust(top=0.85)
	ax.set_title('Average time = '+average+'\n'+'Most common day (Monday=0, Sunday=6) = '+str(most_common_day))

	ax.set_xlabel('Date')
	ax.set_ylabel('Time')

	ax.xaxis_date()
	ax.yaxis_date()

	ax.plot_date(x, y, color='red', label="Person1")

	red_patch = mpatches.Patch(color='red', label="Person1")
	plt.legend([red_patch], ["Person1"])

	plt.show()
	
	json_data.close()

msg_vs_date(person1_date_count, person2_date_count)
date_vs_time(person1_file)