import os
import json 
import requests
import argparse
import platform
import sys 
#import shlex, subprocess

sistema = format(platform.system())

if (sistema == "Linux"):
	# Text colors
	normal_color = "\33[00m"
	info_color = "\033[1;33m"
	red_color = "\033[1;31m"
	green_color = "\033[1;32m"
	whiteB_color = "\033[1;37m"
	detect_color = "\033[1;34m"
	banner_color="\033[1;33;40m"
	end_banner_color="\33[00m"
elif (sistema == "Windows"):
	normal_color = ""
	info_color = ""
	red_color = ""
	green_color = ""
	whiteB_color = ""
	detect_color = ""
	banner_color=""
	end_banner_color=""

def banner():

    print (banner_color + " __  __             _        ____  _                 _ _   _                       _ " + end_banner_color) 
    print (banner_color + "|  \/  | __ _  __ _(_) ___  | __ )| | ___   ___   __| | | | | ___  _   _ _ __   __| |" + end_banner_color)
    print (banner_color + "| |\/| |/ _` |/ _` | |/ __| |  _ \| |/ _ \ / _ \ / _` | |_| |/ _ \| | | | '_ \ / _` |" + end_banner_color)
    print (banner_color + "| |  | | (_| | (_| | | (__  | |_) | | (_) | (_) | (_| |  _  | (_) | |_| | | | | (_| |" + end_banner_color)
    print (banner_color + "|_|  |_|\__,_|\__, |_|\___| |____/|_|\___/ \___/ \__,_|_| |_|\___/ \__,_|_| |_|\__,_|" + end_banner_color)
    print (banner_color + "              |___/                                                                  " + end_banner_color)
    print (" ")
    print (" ")


def is_valid_json(data):
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False


def checkArgs():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description=red_color + 'Magic BloodHound 1.0\n' + info_color)
    parser.add_argument('-f', "--file", action="store",dest='file',help="ZIP File to ingest in BloodHound")
    parser.add_argument("--host", action="store",dest='host',help="Host that runs BloodHound API in format http[s]://domain.tld:port by default: http://localhost:8080")
    parser.add_argument("--path-da", action="store_true",dest='pathda',help="Search a path from any user to Domain Admin reading users.json file")
   
    args = parser.parse_args()
    if (len(sys.argv)==1) or args.file==False:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return args

def login(host):
    loginPayload = {
	"login_method": "secret",
        "secret": "<here_your_password>",
	"username": "admin"
    }
    #print ("[+] Host: " + host + "/api/v2/login")
    try:
    	response = requests.post(host+'/api/v2/login', json=loginPayload)
    	response_content = response.content.decode('utf-8')
    	json_obj = json.loads(response_content)
    	session_token = json_obj['data']['session_token']
    except:
    	print (red_color + "[-] Error during sending the web request.")
    	return 0
    	
    
    return session_token

def get_json_files_in_directory(directory):
    json_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            json_files.append(filename)
    return json_files

def start_upload(filename, token, host):
    url = host+"/api/v2/file-upload/start"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "bhe-python-sdk 0001",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    return response

def upload_data(filename, token, uploaded_id,host):
	url = host+"/api/v2/file-upload/" + str(uploaded_id)


	print (green_color + "[+] " + whiteB_color + "Analizing the file " + green_color + filename)

	#This sed commands is in order to sanitize the JSON's with values recommended by specterops in his Slack channel.
	os.system('sed \'s/"TrustDirection":[3-9]/"TrustDirection":"Disabled"/g\' ' + filename + ' > ' + filename + '-bh-sanitized')
	os.system('sed \'s/"TrustType":[0-9]/"TrustType":"Unknown"/g\' ' + filename + '-bh-sanitized > ' + filename)

	#command = shlex.split('sed \'s/"TrustDirection":[3-9]/"TrustDirection":"Disabled"/g\' ' + filename + ' > ' + filename + '-bh-sanitized')
	#print(command)
	#subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
	#command = shlex.split('sed \'s/"TrustType":[0-9]/"TrustType":"Unknown"/g\' ' + filename + '-bh-sanitized > ' + filename)
	#subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

	#Delete utf-8 signature in order to avoid the first 3 bytes.
	os.system("dd if=" + filename + " of="+filename+"-bh bs=3 skip=1 > /dev/null 2>&1")

	#with open(filename, "r") as myfile:
	#	json_data = myfile.read()
	#	if json_data.startswith('\ufeff'):
	#		json_data = json_data[1:]
	#	json_data = json_data.encode("utf-8").decode('utf-8-sig')
		
	with open(filename+"-bh", "r", encoding="iso-8859-1") as file:
		json_data = file.read()

		if (is_valid_json(json_data)):
	   		print (green_color + "\t[+] " + whiteB_color + "The json is valid! The tool is uploading to BloodHound CE...")
		else:
	    		print (red_color + "\t[-] " + whiteB_color + "This json is NOT valid!!")
    	
	#with open(filename, "r", encoding="utf-8-sig") as file:
    	#	json_data = json.load(file)
    	#	if isinstance(json_data, dict):
    	#		print(green_color + "\t[+] " + whiteB_color + "The json is valid! The tool is uploading to BloodHound CE...")
    	#	else:
    	#		print(red_color + "\t[-] " + whiteB_color + "This json is NOT valid!!")

    	
    	
	file.close()
    	   

	#with open(filename, "r", encoding="iso-8859-1") as myfile2:
		#def chunk_generator():
    		#	chunk_size = 1024
    		#	while True:
    		#		data_chunk = myfile2.read(chunk_size)
    		#		if data_chunk.startswith('\ufeff'):
    		#			data_chunk = data_chunk[1:]
    		#		data_chunk = data_chunk.encode('utf-8').decode('utf-8-sig')
    		#		if not data_chunk:
    		#			break
    		#		yield data_chunk

	    
	headers = {
		"Authorization": f"Bearer {token}",
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
		"Accept": "application/json, text/plain, */*",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"Referer": "http://localhost:8080/ui/administration/file-ingest",
		"Content-Type": "application/json",
		"Origin": "http://localhost:8080",
		"Connection": "close",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-origin"
	}

	os.system("rm -rf " + filename + "-bh*")

	try:
		#response = requests.post(url, headers=headers, data=chunk_generator())
		response = requests.post(url, headers=headers, data=json_data)
	except:
		print (red_color + "[-] Error during sending the web request, Exiting...")
	    	
	return response

def finish_upload_data(filename, token, uploaded_id,host):
    url = host+"/api/v2/file-upload/" + str(uploaded_id) + "/end"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "bhe-python-sdk 0001",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    return response
    
def search_sids(filename):
	with open(filename, "r", encoding="iso-8859-1") as myfile:
		json_data = myfile.read()
		data = json.loads(json_data)
		#object_identifiers = [entry["ObjectIdentifier"] for entry in data["data"]]
		object_identifiers = [entry["Properties"]["name"] for entry in data["data"]]
		
		return object_identifiers
		
def search_path_to_da(sid, token):
	url = host+"/api/v2/groups/"+sid+"/admin-rights"
	headers = {
		"Authorization": f"Bearer {token}",
		"User-Agent": "bhe-python-sdk 0001",
		"Content-Type": "application/json"
	}

	response = requests.get(url, headers=headers)
	
	print (response.text)
	
def search_path_to_da_cypher(user, da_group, token):
	url = host+"/api/v2/graphs/cypher"
	headers = {
		"Authorization": f"Bearer {token}",
		"User-Agent": "bhe-python-sdk 0001",
		"Content-Type": "application/json"
	}
	
	data = "{\"query\": \"MATCH (user:User {name: '"+user+"'})-[*1..10]->(da:Group {name: '"+da_group+"'}) MATCH p = shortestPath((user)-[*]->(da)) RETURN p LIMIT 1\"}"
	
	response = requests.post(url, data=data, headers=headers)
	results = response.text
	
	if '"nodes":{}' not in results:
		print (green_color + "[+] " + whiteB_color + " Path to DA discovered from the user: " + info_color + user)
	
	#Sleep in order to avoid response with status code 429 (Too many requests)
	os.system("sleep 0.5")

def search_da_group(filename):
	with open(filename, "r", encoding="iso-8859-1") as myfile:
		json_data = myfile.read()
		data = json.loads(json_data)
		groups = [entry["Properties"]["name"] for entry in data["data"]]
		for group in groups:
			group_lower = group.lower()
			if ("domain admin" in group_lower):
				return group

#Main
banner()
args = checkArgs()
if (args.host):
	host = args.host
	lastchar = len(host)
	if (host[lastchar-1] == "/"):
		host = host[0:len(host)-1]
else:
	host = "http://localhost:8080"

inicio = args.file.find(".zip")
if (inicio != -1):
	os.system("unzip -q " + args.file)

current_directory = os.getcwd()
json_files = get_json_files_in_directory(current_directory)


token = login(host)
group = ""
totalusers = 0
totalgroups = 0
names = []
group = [] 

for filename in json_files:
	#try:
		if (args.pathda):
			if "users" in filename:
				os.system("dd if=" + filename + " of="+filename+"-bh bs=3 skip=1 > /dev/null 2>&1")
				names = search_sids(filename+"-bh")
				
			if "group" in filename:
				os.system("dd if=" + filename + " of="+filename+"-bh bs=3 skip=1 > /dev/null 2>&1")
				group = search_da_group(filename+"-bh")
			
			totalusers = len(names)
			totalgroups = len(group)
			if (totalusers > 0 and totalgroups > 0):
				for name in names:
					group_da = search_path_to_da_cypher(name,group,token)

		else:
			response = start_upload(filename, token, host)
			json_data = json.loads(response.text)
			uploaded_id = json_data["data"]["id"]
			response2 = upload_data(filename, token, uploaded_id, host)
			print (green_color + "\t[+] " + whiteB_color + "File " + info_color + str(filename) + whiteB_color + " uploaded successfully! BloodHound is ingesting now :)")
			print (" ")
			response3 = finish_upload_data(filename, token, uploaded_id, host)
	#except Exception as e:
	#	print (e)
		#print (red_color + "[-] File " + info_color + str(filename) + whiteB_color + " can't be upload correctly. BloodHound is not analyzing data! :(")

    
os.system("rm -rf *_*.json*")
