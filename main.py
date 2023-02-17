import csv
import pandas as pd

columns: list[str] = [ "MSISDN", "NOM ABONNE", "LOGIN RECRUTEUR", "STATUT APPEL", "DATE RAPPEL", "HEURE RAPPEL", "IDENTITE", "PRIX SIM", "COMPTE MOOV MONEY", "CHANGEMENT MDP", "OPERATION MOOV MONEY", "UTILISE INTERNET", "CONFIGURATION INTERNET", "FORFAIT INTERNET", "FORFAIT VOIX", "PREOCCUPATION", "AGENT", "NOM PRENOM AGENT"]

def transform(item):
   [hour, minutes, seconds] = item.split(':');
   return int(hour) * 3600 + int(minutes) * 60 + int(seconds)

pointcall_db: pd.DataFrame = pd.read_csv('data/pointcall.csv', sep=";")
foniva_db: pd.DataFrame = pd.read_csv('data/foniva.csv', sep=",")

foniva_db = foniva_db[foniva_db['Result'] == "ANSWER"]
foniva_db['Total dial Duration (int)'] = foniva_db['Total dial Duration'].map(transform)
foniva_db = foniva_db[foniva_db['Total dial Duration (int)'] > 30]

final_result: pd.DataFrame = pd.merge(pointcall_db, foniva_db, how="inner", right_on="Called", left_on="MSISDN")
final_result = final_result[columns]
final_result.to_csv('POINTCALL_DEF.csv', sep=";", quoting=csv.QUOTE_ALL)
print(final_result)
