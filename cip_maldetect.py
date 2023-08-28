import requests
import csv
import time
import re
import os
import pyclamd

## you have to rewrite the path for your own directory route, query and api key
c2ip_file_name = rf"C:\Users\{USERNAME}\Desktop\tmp\Leaked_IP.csv"
malinfo_file_name = rf"file_result.csv"
file_save_path = f"C:\\Users\\{USERNAME}\\Desktop\\tmp\\"
ipsearch_query = "tag:c2 status_code:200"
Criminal_IP_API_KEY = "<YOUR_CriminalIP_API_KEY>"
##

c2ip_csv_format = ["IP address", "Open Port", "Title"]
malinfo_csv_format = ["IP address", "Open Port", "Filename", "Malicious-Status"]

def print_banner():
    print()
    print("██████╗██╗██████╗     ██████╗ ███████╗████████╗███████╗ ██████╗████████╗ ██████╗ ██████╗ ")
    print("██╔════╝██║██╔══██╗    ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗")
    print("██║     ██║██████╔╝    ██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║   ██║██████╔╝")
    print("██║     ██║██╔═══╝     ██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗")
    print("╚██████╗██║██║         ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║")
    print("╚═════╝╚═╝╚═╝         ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝")
    print()

with open(c2ip_file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(c2ip_csv_format)
    
with open(malinfo_file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(malinfo_csv_format)
   
    
payload={}
headers = {
  "x-api-key":Criminal_IP_API_KEY 
}
def read_csv(csv_name, row_num):
    result =[]
    
    with open (csv_name, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for _ in range(row_num-1):
            next(reader)
               
        row = next(reader, None)
        
        if row:
            ip=row[0]
            port=row[1]
            return (ip, port)
        else:
            return None


def download_file(download_url, save_path, max_file_size=50 * 1024 * 1024, timeout=30, max_retries=2):
    #File size limit: 50MB, Response time limit: 30 seconds, Maximum 2 download attempts.
    headers = {'User-Agent': 'Mozilla/5.0'}  # add User-Agent header

    for attempt in range(max_retries):
        try:
            with requests.get(download_url, stream=True, headers=headers, timeout=timeout) as response:
                response.raise_for_status()

                content_length = response.headers.get('content-length')
                if content_length and int(content_length) > max_file_size:
                    print(f"download fail: {save_path} is too big to download!!!")
                    return False

                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                with open(save_path, 'wb') as file:
                    total_size = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                        total_size += len(chunk)

                        print(f"now downloading... {total_size}/{content_length}", end='\r')

                print(f"\ndownload complete : {save_path}")
                time.sleep(10)
                return True

        except requests.exceptions.Timeout:
            print("download timeout : response takes too long")
            return False

        except requests.exceptions.RequestException as e:
            print(f"download fail: {e}")
            if attempt < max_retries - 1:
                print("retrying...")
                time.sleep(5)
            else:
                return False

    return False


def is_malicious(file_path):
    print("now scanning...")
    try:
        cd = pyclamd.ClamdNetworkSocket()
        scan_result = cd.scan_file(file_path)
        if scan_result is not None:
            if file_path in scan_result and scan_result[file_path][0] == 'FOUND':
                print(f"!!! MALWARE DETECTED : {scan_result[file_path][1]}")
                return True, scan_result[file_path][1]
            else:
                print(f"ERROR OCCURRED: {scan_result[file_path][1]}")
                return False, scan_result[file_path][1]
        else:
            print("MALWARE WAS NOT DETECTED.")
            return False, "No suspicious code detected"
    except pyclamd.ConnectionError:
        print("cannot connect to ClamAV server")
        return False
    
    
def find_directory_listing_IP():
    banner_search_url = "https://api.criminalip.io/v1/banner/search"
    banner_search_params = {
    "query" : ipsearch_query,
    "offset" : 0
    }
    response = requests.request("GET", banner_search_url, headers=headers, data=payload, params=banner_search_params)#, timeout=5)
    time.sleep(0.5)
    if response.json()["status"]==200:
        offset_count = int(response.json()["data"]["count"]/100)+1
        print("total requests count : " + str(offset_count))
        for i in range(offset_count):
            banner_search_params = {
            "query" : "tag:c2 status_code:200",
            "offset" : i*100
            }
            response2 = requests.request("GET", banner_search_url, headers=headers, data=payload, params=banner_search_params)#, timeout=5)
            time.sleep(0.5)
            if response2.json()["status"]==200:
                data=response2.json()["data"]
                results = data["result"]
                for result in results:
                    if "Index of" in str(result["title"]) or "Directory listing for" in str(result["title"]): 
                        tmp_csv = [result["ip_address"], result["open_port_no"], result["title"]]                   
                        with open(c2ip_file_name, 'a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow(tmp_csv)
            else:
                print(response2.json()["status"])
                print(response2.json()["message"])
            print(f"{offset_count - i - 1} requests left")
    else:
        print(response.json()["status"])
        print(response.json()["message"])
    print("c2 detect end")    

def download_and_define(file_name):
    start_string = "<a href=\""
    end_string = "\">"
    pattern = re.compile(f"{start_string}(.*?){end_string}")
    row_counter = 1
    while True:
        if read_csv(file_name, row_counter) == None:
            print("search end!")
            break
        now_ip, now_port = read_csv(file_name, row_counter)
        row_counter = row_counter+1

        print("currunt address : " + str(now_ip)+":" + str(now_port))
        
        ip_search_url = "https://api.criminalip.io/v1/ip/data"
        ip_search_params = {
            "ip":str(now_ip)
        }
        try:
            response=requests.request("GET", ip_search_url, data=payload, headers=headers, params=ip_search_params, timeout = 5)
            if response.json()["status"] == 200:
                port = response.json()["port"]
                datas = port["data"]
                banner=""
                for data in datas:
                    if data["open_port_no"] == int(now_port):
                        banner = data["banner"]
                        break
                    else:
                        continue
                result = pattern.findall(banner)           
                for name in result:
                    if ".zip" in name or ".exe" in name or ".sh" in name:
                        if str(now_port) == "443":
                            current_path = f"https://{str(now_ip)}:{str(now_port)}/{name}"
                        else:
                            current_path = f"http://{str(now_ip)}:{str(now_port)}/{name}"
                        save_path = f"{file_save_path}{str(now_ip)}_{str(now_port)}\\{str(name)}"
                        print("-------------------------------------------------")
                        print(f"This is save path : {save_path}")
                        if now_port != "443":
                            dlr = download_file(current_path, save_path) #download files
                            time.sleep(0.5)
                            if dlr == True:
                                mal_result = is_malicious(save_path) #detect malware
                                print(f"This is mal result for {save_path} : {mal_result}")
                                if mal_result[0] == True:
                                    print(f"{name} is malicious!")
                                    print(name, mal_result[1])
                                    mal_csv = [now_ip, now_port, name, mal_result[1]]
                                    with open(malinfo_file_name, 'a', newline='') as file:
                                        writer = csv.writer(file)
                                        writer.writerow(mal_csv)
                                else:
                                    if "path check" not in mal_result[1]: 
                                        print(f"{name} is not malicious!")
                                        mal_csv = [now_ip, now_port, name, mal_result[1]]
                                        with open(malinfo_file_name, 'a', newline='') as file:
                                            writer = csv.writer(file)
                                            writer.writerow(mal_csv) #save data
                            else:
                                print("download FAIL!! Cannot scan file!!")
                        print("-------------------------------------------------")
            else:
                print(response.json()["status"])
                print(response.json()["message"])          
        except requests.exceptions.Timeout:
            print("The request did not receive a response within 10 seconds.")
                  
                    
if __name__ == "__main__":
    print_banner()
    find_directory_listing_IP()
    download_and_define(c2ip_file_name)   
    print("Malware detect END")