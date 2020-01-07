'''
statsbasic.py

Performs basic analysis against databases populated by getstats.py

1/7/2020 -- Progress so far:

High Level things To Do:
Print top 10 Players by stat
Print sum of a stat for all players or a configurable subset
...?

'''

import sqlite3
import pandas as pd

conn = sqlite3.connect('stats.sqlite')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def printMenu():
    print('[1] TopN Stats')
    print('[2] Summary Stats')

def printColumn():
    cur.execute('SELECT * FROM ' + table + ' where id=1')
    col = cur.fetchall()
    for i in col:
        dic = dict(i)
        for key in dic:
            if key != 'id' and key != 'Player' and key != 'Pos' and key != 'Tm':
                print(key)

def topN(sample, field):
    cur.execute('SELECT Player, Pos, {field} FROM {table} ORDER BY {field} DESC LIMIT {sample}'.format(field=field, table=table, sample=sample))
    return cur.fetchall()

def summary(sample, field):
    x = 0
    cur.execute('SELECT Player, Pos, {field} FROM {table} ORDER BY {field} DESC LIMIT {sample}'.format(field=field, table=table, sample=sample))
    result = cur.fetchall()

    for row in result:
        x = x + row[field]

    return x

table = input('Enter Table Name for Analysis: ')
if len(table) < 1:
    table = 'Passing'

while True:
    printMenu()
    sel = input('> ')

    if sel == '1':
        x = input('How Many Players ( top 1-n ): ')

        printColumn()

        y = input('Which Stat: ')

        result = topN(x,y)
        for row in result:
            row = dict(row)
            print(row)

    elif sel == '2':
        statsum = 0
        x = input('How Many Players ( top 1-n ): ')

        printColumn()

        y = input('Which Stat: ')

        statsum = summary(x,y)
        print('\nThe Total {stat} for the top {num} players is {result}'.format(stat=y, num=x, result=statsum) )

    elif sel == 'exit':
        exit()
    else:
        print('Invalid Selection!\n')

    print('\n')
