#Robert Williams 2/9/26
#ITIS 3200 Lab 2
#Uses hashli to encrypt and verify files
# credit to https://www.geeksforgeeks.org/python/python-program-to-find-hash-of-file/
# used as a reference for accessing files and how to use hashlib to hash files

import json
import hashlib
from pathlib import Path

#config

ramUsage = 4096
algoritim = "sha256"


def hash_file(filename):

    hash = hashlib.new(algoritim)

    #opens files in binary
    with open(filename, "rb") as file:

        #loops through file sized for ram and hashes it
        chunk = 0
        while chunk != b'':
            chunk = file.read(ramUsage)
            hash.update(chunk)

    return hash.hexdigest()

def traverse_directory(directory):

    fileHashes = {}

    #traverses directory and subdirectories
    #may not be appropriate for very large directories
    for file in directory.rglob("*"):
        if file.is_file():

            #calls hash function
            print(f"Hashing file: {file}")
            fileHash = hash_file(file)

            print(f"Hash: {fileHash}")
            
            #stores hash to dictrionary withh full file directory
            if fileHash: 
                fileHashes[str(file.resolve())] = fileHash

    return fileHashes

def directory_handler():
    #asks user for directory and checks if it is valid
    directory = input("Enter the directory: ").strip()
    directory = Path(directory)

    if not directory.is_dir():
        print("Invalid directory")
        return False
    return directory

def generate_table():
    print("Generate mode")

    directory = directory_handler()

    if not directory:
        return
    
    fileHashes = traverse_directory(directory)

    dirPath = directory.resolve()
    outputFile = dirPath / 'hashes.json'
    

    #saves hashes to json file
    with open(outputFile, 'w') as jsonFile:
        json.dump(fileHashes, jsonFile)
    print(f"Hashes saved to {outputFile}")

def validate_table():
    print("Validation mode")
    
    #get directory and check for json file
    directory = directory_handler()
    if not directory:
        return
    if not (directory.resolve() / 'hashes.json').exists():
        print("No hashes.json file found in directory")
        return
    
    #store and create json file object
    with (directory / 'hashes.json').open("r") as jsonFile:
        collectedHashes = json.load(jsonFile)

    #traverse directory and compare hashes
    for file in directory.rglob("*"):

        if file.is_file():

            fileHash = hash_file(file)

            if str(file.resolve()) in collectedHashes: 

                if fileHash != collectedHashes[str(file.resolve())]:
                    print(f"File {file} is invalid")
                else:
                    print(f"File {file} is valid")
            else:
                print(f"File {file} is not in the collected hashes and may be new")

def main():

    print(f"Using algorithm: {algoritim}")
    print(f"RAM usage limit: {ramUsage} bytes")

    mode = input("Enter mode Generate 1/Validate 2: ")
    match mode:
        case '1':
            generate_table()
        case '2':
            validate_table()
        case _:
            print("Invalid mode")

if __name__ == "__main__":
    main()