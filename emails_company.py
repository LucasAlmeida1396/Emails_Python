import sqlite3, re

list_email = {}
email_novo = ''
qtd = 0
list_company = []

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox-short.txt'
fh = open(fname)

for line in fh:
    email_novo = re.findall('From: (\S+@\S+)', line)
    if email_novo:
        email_novo = email_novo[0]
        if email_novo in list_email:
            list_email[email_novo]["counts"] += 1
        else:
            list_email[email_novo] = {"email": email_novo, "counts": 1}

lista_final_email = list(list_email.values())

lista_emails_ordenada = sorted(lista_final_email, key=lambda x: x['counts'], reverse=True)

for each in lista_emails_ordenada:
    company = re.findall('@(\S+)', each['email'])

    if not list_company:
        list_company.append({'company': company[0], 'counts': each['counts']})
    else:
        company_set = {i['company'] for i in list_company}
        if company[0] in company_set:
            for i in list_company:
                if company[0] == i['company']:
                    i['counts'] += each['counts']
                    break
        else:
            list_company.append({'company': company[0], 'counts': each['counts']})

lista_company_ordenada = sorted(list_company, key=lambda x: x['counts'], reverse=True)

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts_emails')
cur.execute('DROP TABLE IF EXISTS Counts_company')
cur.execute('CREATE TABLE Counts_emails (email TEXT, count INTEGER)')
cur.execute('CREATE TABLE Counts_company (email TEXT, count INTEGER)')

for e in lista_emails_ordenada:
    cur.execute('INSERT INTO Counts_emails (email, count) VALUES (?, ?)', (e['email'], e['counts']))

for c in lista_company_ordenada:
    cur.execute('INSERT INTO Counts_company (email, count) VALUES (?, ?)', (c['company'], c['counts']))

conn.commit()

cur.close()