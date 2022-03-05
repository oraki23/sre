import json
import requests
import csv


def compileAuthorsDate(dictfiles, lsttokens, repos):
    ct = 0  # token counter
    for repo in repos:
        repo_name = repo.split('/')[-1]
        with open(f'partie1/{repo_name}.csv') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ipage = 1  # url page counter
                print(row)
                while True:
                    if ct == len(lstTokens):
                        ct = 0
                    spage = str(ipage)
                    file_path=row[0]
                    commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + \
                         '&per_page=100&path=' + file_path
                    headers = {'Authorization': 'token ' + lsttokens[ct]}
                    ct += 1
                    content = requests.get(commitsUrl, headers=headers)
                    jsonCommits = json.loads(content.content)
                    if len(jsonCommits) == 0:
                        break
                    for commitObj in jsonCommits:
                        authorObj = commitObj['commit']['author']
                        info = (authorObj['name'], authorObj['date'])
                        print(info)
                        if(file_path not in dictfiles):
                            dictfiles[file_path] = []
                        dictfiles[file_path].append(info)
                    ipage+=1
                

# repo = 'scottyab/rootbeer'
# put your tokens here
lstTokens = ['']


dictfiles = dict()
compileAuthorsDate(dictfiles, lstTokens, ['k9mail/k-9'])

fileoutput = 'data_k-9.csv'
rows = ["Filename", "Author", "Commit Date"]
fileCSV = open(fileoutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for filename, infos in dictfiles.items():
    for info in infos:
        rows = [filename, info[0], info[1]]
        writer.writerow(rows)
fileCSV.close()
print("Done")
# countfiles(dictfiles, lstTokens, repo)
# print('Total number of files: ' + str(len(dictfiles)))

# file = repo.split('/')[1]
# #change this to the path of your file
# fileOutput = file+'.csv'
# rows = ["Filename", "Touches"]
# fileCSV = open(fileOutput, 'w')
# writer = csv.writer(fileCSV)
# writer.writerow(rows)

# bigcount = None
# bigfilename = None
# for filename, count in dictfiles.items():
#     rows = [filename, count]
#     writer.writerow(rows)
#     if bigcount is None or count > bigcount:
#         bigcount = count
#         bigfilename = filename
# fileCSV.close()
# print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')