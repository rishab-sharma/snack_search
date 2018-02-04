#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 17:57:22 2018

@author: rishab
"""
import sqlite3
import pandas as pd
import io

database = "database/snack_search"

connection = sqlite3.connect('{}.db'.format(database))
connection.text_factory = str
c = connection.cursor()

def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS recepies( recepie_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT , protein TEXT , fat TEXT , calories TEXT , sodium TEXT , dr_f1 TEXT , dr_f2 TEXT  , types TEXT)") # INTEGER PRIMARY KEY AUTOINCREMENT


if __name__ == '__main__':
    create_table()
    
    df = pd.read_csv('ML/40_labels.csv',sep = ',')
    
    title = df['title']
    calories = df['calories']
    protein = df['protein']
    fat = df['fat']
    sodium = df['sodium']
    dr_f1 = df['DR_f1']
    dr_f2 = df['DR_f2']
    types = df['TYPE']
    
    
    for i in range(len(types)):
        ti = title[i]
        ca = calories[i]
        pr = protein[i]
        fa = fat[i]
        so = sodium[i]
        d1 = dr_f1[i]
        d2 = dr_f2[i]
        ty = types[i]
        sql = """INSERT INTO recepies (title , protein , fat , calories , sodium , dr_f1 , dr_f2 , types) VALUES (? , ? , ? , ? , ? , ? , ? , ?);"""
        try:
            c.execute(sql , (ti , pr , fa , ca , so , d1 , d2 , ty))
            print "Done Loop no. {}".format(i)
        except Exception as e:
            print str(e)
        connection.commit()
