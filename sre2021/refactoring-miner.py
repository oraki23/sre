import json
from pip._vendor import requests

f = open('data.json')
data = json.load(f)

nbRefactor = 0
nbFiles = 0
nbCommits = 0

dictRefactoring = dict()
filesRefactoring = dict()
authorsRefactoring = dict()

repo = 'hscrocha/jpacman'
lstTokens = ['']

for commit in data['commits']:
    for refactoring in commit['refactorings']:
        type = refactoring['type']
        dictRefactoring[type] = dictRefactoring.get(type, 0) + 1

        if(len(refactoring['leftSideLocations']) > 0):
            filePath = refactoring['leftSideLocations'][0]["filePath"]
            filesRefactoring[filePath] = filesRefactoring.get(filePath, 0) + 1
            nbFiles += 1
        nbRefactor += 1
    nbCommits += 1

    if(len(commit['refactorings']) > 0):
        commitSha = commit['sha1']
        # For each commit, use the GitHub commit API to extract the files touched by the commit
        shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + commitSha
        headers = {'Authorization': 'token ' + lstTokens[0]}
        content = requests.get(shaUrl, headers=headers)
        shaDetails = json.loads(content.content)
        commitAuthorName = shaDetails['commit']['author']['name']

        authorsRefactoring[commitAuthorName] = authorsRefactoring.get(commitAuthorName, 0) + 1
        print('author name: ' + commitAuthorName + ' commit : ' + str(nbCommits) + '/' + str(len(data['commits'])))

dictRefactoringSorted = {k: v for k, v in sorted(dictRefactoring.items(), key=lambda item: item[1])}

filesRefactoringSorted = {k: v for k, v in sorted(filesRefactoring.items(), key=lambda item: item[1])}

authorsRefactoringSorted = {k: v for k, v in sorted(authorsRefactoring.items(), key=lambda item: item[1])}

for refactoringType, count in dictRefactoringSorted.items():
    print(refactoringType + ': ' + str(count))

for refactoredFile, count in filesRefactoringSorted.items():
    print(refactoredFile + ': ' + str(count))

for refactoringAuthor, count in authorsRefactoringSorted.items():
    print(refactoringAuthor + ': ' + str(count))

print('Nb of files: ' + str(nbFiles))
print('Nb of Refactor: ' + str(nbRefactor))
print('Nb of Commits: ' + str(nbCommits))