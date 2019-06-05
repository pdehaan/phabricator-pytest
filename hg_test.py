import hgapi

print(hgapi.hg_version())

"""
repo = hgapi.Repo("peter")  # existing folder

# repo.hg_init()
repo.hg_add("file2.txt")  # already created but not added file
# repo.hg_commit("Adding file2.txt", user="me")

print(str(repo['tip'].desc))
# 'Adding file.txt'

print(len(repo[0:'tip']))
# 1
"""
