#!/usr/bin/env python

import pandas as pd
import os
import sys

columns = ["taskid", "category", "country", "state", "city", "varname", "value"]

master_csv = "master.csv"

if os.path.exists(master_csv):
    df = pd.read_csv(master_csv)
else:
    df = pd.DataFrame([], columns=columns)

filename = sys.argv[1]

if os.path.exists(filename):
    new_data = pd.read_csv(filename, sep="|")
else:
    exit(1)

for i in range(new_data.shape[0]):
    row = new_data.iloc[i]
    taskid = row.taskid
    category = row.category
    country = row.country
    state = row.state
    city = row.city
    varname = row.varname
    comment = row.comment
    comment = "\n".join(comment.split("\n")[1:-1])

    os.system("clear")
    if int(taskid) in df.taskid.values:
        continue
    msg = """ TASKID   : {taskid}
 URL      : https://clas.teamwork.com/#tasks/{taskid}
 CATEGORY : {category}
 COUNTRY  : {country}
 STATE    : {state}
 CITY     : {city}
 VARNAME  : {varname}
 
 COMMENT
 =======
 \033[96m{comment}\033[0m""".format(taskid=taskid,category=category,country=country,state=state,city=city,varname=varname, comment=comment)
    print(msg)
    result = raw_input("Value >> ")
    print("\033[31m===========================================================\033[0m")
    if not result:
        continue
    new_row = pd.DataFrame([[taskid, category, country, state, city, varname, result]], columns=columns)
    df = df.append(new_row)
    df.to_csv(master_csv, index=False)
