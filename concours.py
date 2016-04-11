""" Analysis of the cnap results 2016 """

import pandas as pd

# Candidats Jury 1:
c1 = pd.read_excel("sousjury1.xlsx")
c1["jury"] = 1
# Candidats Jury 2:
c2 = pd.read_excel("sousjury2.xlsx")
c2["jury"] = 2
# All candidates:
candidats = pd.concat([c1, c2])
# improve column names:
candidats = candidats.rename(columns={candidats.columns[0]: 'nom', candidats.columns[1]: 'prenom'})

#candidats["fullName"] = candidats.nom +" "+ candidats.prenom

from mechanize import Browser
br = Browser()


for index, candidat in candidats.iterrows():
    nameLinkPrefix = "http://www.theses.fr/?q="+candidat.nom+"+"+candidat.prenom
    print nameLinkPrefix
