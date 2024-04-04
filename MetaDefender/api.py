import requests
import time
import os

api_url = "https://api.metadefender.com/v4/"

# main 
class MetaDefender_api():
    def Apikey_info(key=""):
        url = api_url+"apikey/"
        try:
            if key == "":
                raise ValueError("no key parsed: key=None")

            header = {
                "apikey": str(key)
            }

            response = requests.get(url, headers=header)
            
            # check if the request was successful
            if response.status_code == 200:
                # format response
                return response.json()
            else:
                return str(response.status_code)
        except Exception as e:
            raise str(e)


    def Apikey_remaining_limits(key=""):
        url = api_url+"/apikey/limits/status"
        try:
            if key == "":
                raise ValueError("no key parsed: key=None")

            header = {
                "apikey": str(key)
            }

            response = requests.get(url, headers=header) 

            # check if the request was successful
            if response.status_code == 200:
                # format response
                return response.json()
            else:
                return str(response.status_code)
        except Exception as e:
            raise str(e)


    def Fetch_analysis_result(dataId, key=""):
        url = api_url+f"/file/{dataId}"
        try: 
            if key == "":
                raise ValueError("no key parsed: key=None")

            header = {
                "apikey": str(key),
                "x-file-metadata": "1"
            } 

            response = requests.get(url, headers=header)

            # check if the request was successful
            if response.status_code == 200:
                # only return results if the file is scanned 100% (loop till 100% is returned)
                while int(requests.get(url, headers=header).json()["scan_results"]["progress_percentage"]) != 100:
                    time.sleep(1)

                # format response
                return requests.get(url, headers=header).json()
            else:
                return str(response.status_code)
        except Exception as e:
            raise e


    def File_Scanning(filepath, password="", samplesharing=1, privateprocessing=0, return_with_results=True, key=""):
        url = api_url+"/file"
        try:
            if key == "":
                raise ValueError("no key parsed: key=None")
            
            # Open the file in binary mode
            # check if the filepath is valid
            if os.path.exists(filepath):
                # Open the file in binary mode
                file = open(filepath, 'rb')
                # Create a dictionary containing the file to be scanned
                files = {'file': file}
            else:
                raise FileNotFoundError("No valid Filepath submitted.")
            
            # get the filename from the string
            filename = os.path.basename(filepath)

            header = {
                "apikey": str(key),
                "filename": str(filename),
                "archivepwd": str(password),
                "filepassword": str(password),
                "samplesharing": str(samplesharing),
                "privateprocessing": str(privateprocessing)
            }

            response = requests.post(url, headers=header, files=files) 

            # close all open files after the request
            file.close()

            # check if the request was successful
            if response.status_code == 200:
                # if return_with_results is off send data
                if not return_with_results:
                    # format response
                    return response.json()
            else:
                return str(response.status_code)
            
            # return_with_results: True proceed
            return MetaDefender_api.Fetch_analysis_result(response.json()["data_id"], key)

        except Exception as e:
            raise e


    def Hash_Lookup(hash, key=""):
        url = api_url+f"/hash/{hash}"
        try:
            if key == "":
                raise ValueError("no key parsed: key=None")
            
            header = {
                "apikey": str(key)
            }

            response = requests.get(url, headers=header)

            # check if the request was successful
            if response.status_code == 200:
                # format response
                return response.json()
            elif response.status_code == 404:
                return str(response.status_code), ":Hash not found?"
            elif response.status_code == 400:
                return str(response.status_code), ":Invalid Hash?"
            else:
                return str(response.status_code)
        except Exception as e:
            raise e