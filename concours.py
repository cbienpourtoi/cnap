""" Analysis of the cnap results 2016 """

import pandas as pd
import sys
from mechanize import Browser

# Candidats Jury 1:
c1 = pd.read_excel("sousjury1.xlsx")
c1["jury"] = 1
# Candidats Jury 2:
c2 = pd.read_excel("sousjury2.xlsx")
c2["jury"] = 2
# All candidates:
candidats = pd.concat([c1, c2], ignore_index = True)
# improve column names:
candidats = candidats.rename(columns={candidats.columns[0]: 'nom', candidats.columns[1]: 'prenom'})

# Correcting name mismatch
errorName = "HUBY ELSA"
errosIndex = candidats[candidats.nom == "HUBY ELSA"].index
candidats = candidats.set_value(errosIndex, "nom","HUBY")
candidats = candidats.set_value(errosIndex, "prenom","ELSA")

#candidats["fullName"] = candidats.nom +" "+ candidats.prenom

# Setup mechanize
br = Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Firefox')]

# Init new values:
candidats["date"] = " "
candidats["domaine"] = "  "
candidats["nom2"] = " "
candidats["link"] = " "

for index, candidat in candidats.iterrows():
    nameFormated = candidat.nom.replace(" ", "+")+"+"+candidat.prenom.replace(" ", "+")
    
    #nameLink = "http://www.theses.fr/?q="+nameFormated
    nameLink = "http://www.theses.fr/?q=&zone1=titreRAs&val1=&op1=AND&zone2=auteurs&val2="+nameFormated+"&op2=AND&zone3=etabSoutenances&val3=&op3=AND&zone4=dateSoutenance&val4a=&val4b="
    
    
    print nameLink
    candidats.set_value(index, "link", nameLink)
    
    line = 0
    
    lineDate = []
    lineDomaine = []
    lineName = []

    html = (br.open(nameLink)).get_data()
    htmlLines = html.split("\n")
    for h in htmlLines:
        if ('class="soutenue"' in h) | ('class="preparation"' in h):
            #h.find("Soutenue"):
            lineDate.append(line)
            #print h
        if '<div class="domaine">' in h:
            #h.find('<div class="domaine">')>=0:
            lineDomaine.append(line+1)
            #print h

        if '<p>par ' in h:
            lineName.append(line)

        line += 1


    if (len(lineDate) != len(lineDomaine)) | (len(lineDate) != len(lineName)) | len(lineDate) == 0:
        print "Mismatch date/domain, or no value: skipping"
    else:

        dates = []
        domaines = []
        names = []
        for lDate, lDomaine, lName in zip(lineDate, lineDomaine, lineName):
            if "outenue" in htmlLines[lDate]:
                dates.append(htmlLines[lDate].replace('<h5 class="soutenue">', '').replace("</h5>\r", ''))
            else:
                dates.append(htmlLines[lDate].replace('<h5 class="preparation">', '').replace("</h5>\r", ''))
            domaines.append(htmlLines[lDomaine].replace('<h5>', '').replace("</h5>\r", ''))
            cleanerName = htmlLines[lName].replace('<p>par <a href=/', '').replace('<p>par ', '') # Replace all this shit by a regex!
            whNameStarts = cleanerName.find(">")
            whNameEnds = cleanerName.find("</a>\r")
            names.append(cleanerName[whNameStarts+1:whNameEnds])
        if len(names) == 0:
            continue
        
        resultPosition = 0
        if nameFormated == "GIRARD+JULIEN":
            resultPosition = 3
        if nameFormated == "FAVRE+CECILE":
            resultPosition = 2
        if nameFormated == "ADAM+REMI":
            resultPosition = 1
        if nameFormated == "BRUN+FRANCOIS":
            resultPosition = 5
        if nameFormated == "PARIS+ISABELLE":
            resultPosition = 1
        if nameFormated == "RODRIGUES+MYRIAM":
            resultPosition = 1
        if nameFormated == "DANIEL+FABIEN":
            resultPosition = 1
        if nameFormated == "DEMANGEON+OLIVIER":
            resultPosition = 1
        if nameFormated == "LOIZEAU+DAMIEN":
            resultPosition = 1
        if nameFormated == "PRAT+VINCENT":
            resultPosition = 1
        
        candidats.set_value(index, "nom2", names[resultPosition])
        candidats.set_value(index, "domaine", domaines[resultPosition])
        candidats.set_value(index, "date", dates[resultPosition])
        print dates[resultPosition], domaines[resultPosition], names[resultPosition]

        #if nameFormated == "DESMARS+JOSSELIN":
        #    sys.exit()


candidats["year"] = candidats.date.str.extract("(19[0-9][0-9]|20[0-9][0-9])")

candidats.to_csv("candidatsAddedValue.csv", index = None, encoding='utf-8')


