```

██████╗██╗██████╗     ██████╗ ███████╗████████╗███████╗ ██████╗████████╗ ██████╗ ██████╗
██╔════╝██║██╔══██╗    ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██║     ██║██████╔╝    ██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║   ██║██████╔╝
██║     ██║██╔═══╝     ██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
╚██████╗██║██║         ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═════╝╚═╝╚═╝         ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝

```

# About

* This tool utilizes Criminal IP API to detect the IP addresses of C2 servers that are directory listed.

* After downloading files from the respective C2 server, it scans for malicious files using clamAV.

* It utilizes Criminal IP's API([https://api.criminalip.io/v1/banner/search](https://api.criminalip.io/v1/banner/search)) to detect the corresponding IPs.

* It utilizes the [https://api.criminalip.io/v1/ip/data](https://api.criminalip.io/v1/ip/data) API to verify the link for file download and download accordingly.

* All resulting values are formatted using the .csv file structure.

* Through this open-source antivirus tool, you can collect malicious samples uploaded to C2 IPs and assess the risk level of those malicious IPs through sample threat analysis.

</br>

# Prerequisites

**Criminial IP API KEY**

* Criminal IP API KEY is needed to use this program. You can obtain it at [Criminalip.io](https://www.criminalip.io) after signing up for a free account.

</br>

**pyclamd module**

* Pyclamd module is needed in order to use clamAV in python.

```
pip install pyclamd
```

</br>

**requests module**

* Requests module is needed to communicate with the web server.

```
pip install requests
```

</br>

* **Clam AV**

    * You need to download clamAV in advance.  → [clamAV download](https://www.clamav.net/downloads)

    * After downloading the installation file that corresponds to your operating system, proceed with the installation (administrator privileges are required).

    </br>

    (마케팅팀 이미지 삽입 필요)


</br>

# Installation and Setup

**Download Repository**

```
git clone repository_address.git (마케팅팀 삽입 필요)
```

**Configure ClamAV**

* Access the folder where clamAV is installed.
   * In most cases it's located in C:\Program Files\ClamAV.
* For conf file configuration, open the 'clamd.conf.sample' and 'freshclam.conf.sample' files with a text editor (code editor). Remove 'Example' on the top, then delete the '.sample'  from both file names and save them in the same place as 'freshclam.exe' and 'clamd.exe'
* The first part of 'clamd.conf.sample' is shown below.
```
##
## Example config file for the Clam AV daemon
## Please read the clamd.conf(5) manual before editing this file.
##


# Comment or remove the line below.
Example

# Uncomment this option to enable logging.
# LogFile must be writable for the user running daemon.
# A full path is required.
# Default: disabled
# LogFile "C:\Program Files\ClamAV\clamd.log"
```
</br>

(마케팅팀 이미지 삽입 필요)

* Run 'cmd(terminal)' as administrator and locate the files to the folder where ClamAV is installed.
```
cd {clamAV folder PATH}
```
</br>

* Enter the **freshclam** command in the respecitve directory and wait until it is completed. Afterward, execute "clamd.exe."

```
freshclam
```

* If 'clamd.exe, port 3310' is in Task manager(Ctrl + Shift + Esc) → Performance → Open Resource Moniter → Network → Listening Ports, clamAV installation and execution is completed. Below is a sample image. 

</br>

(마케팅팀 이미지 삽입 필요)

* Alternatively, you can verify the installation and execution by using the following command in the terminal.
```
netstat -nao | find "3310"
```
(마케팅팀 이미지 삽입 필요)
</br>
* If the status of 127.0.0.1:3310 is 'Listening' as shown above, you can conclude that the installation has been successfully completed.

</br>

**Filepath & API key Setting**
* Before running the program, you need to insert the path and API key using a text editor (code editor).

* The following paths and variable settings are required at the top of the 'cip_maldetect.py' code.
  
    * c2ip_file_name : the path and filename where the .csv file, storing IP address infomation detected with the Directory Listing, will be saved
   
    * malinfo_file_name : the path and filename where the .csv file, storing the detection results of the downloaded files, will be saved
  
    * file_save_path = the path for downloading files from the web server detected with the Directory Listing
   
    * ipsearch_query : a search query used for dectecting c2 ip that is Directory Listed
  
    * Criminal_IP_API_KEY : key for using Criminal IP API

(마케팅팀 이미지 삽입 필요)


</br>

# How to get started & screenshot

* **Execution Example**

**Program Execution** 

```
python cip_maldetect.py
```
A banner "CIP DETECTOR" will be displayed when the program is executed. 

Afterwards, the program will display the total number of requests required for collecting C2 IPs, followed by indicating the current count of remaining requests. 

(마케팅팀 이미지 삽입 필요)

</br>

With each completed request, the returned IP information based on the 'ipsearch_query' will be saved in the 'Leaked_IP.csv' file in the following format. 

|IP Address|Open Port|Title|
|----------|---------|-----|

(마케팅팀 이미지 삽입 필요)

</br>

Once the IP information collection is completed, the program will proceed to download .exe, .sh, and .zip files from the server, which are stored in the folder generated based on the IP information.

The file storing process is shown in the following image.

(마케팅팀 이미지 2개 삽입 필요)

</br>

After the download is completed, the program will use clamAV to perform a scan for malicious files. Once the scan is complete, the relevant information will be stored in the 'file_result.csv' file.

The format of the 'file_result.csv' used in the example is shown in the following image. You can review the files identified as malicious code.

|IP Address|Port|File Name|Result|
|----------|----|---------|------|

(마케팅팀 이미지 삽입 필요)

</br>

While the above process is in progress, the terminal will provide information about file storage paths, download status, scanning status, and the results of the current IPs and files.

Below is an example image of the information provided in the terminal as the program is running.

(마케팅팀 이미지 삽입 필요)

