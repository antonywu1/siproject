import unittest
import sqlite3
import json
import os
import requests
import re

def main():
    conn = sqlite3.connect('covid.db')
    c = conn.cursor()

    c.execute("SELECT Covid_Data.date, Covid_Data.newCases, Stock_Data.changePrice FROM Covid_Data JOIN Stock_Data ON Covid_Data.date = Stock_Data.date")
        
    results = c.fetchall()
    conn.close()
    print(results)

    avgChangePerMonth = {}
    sum_change = 0
    day_counter = 0
    curr_month = 1
    for day in results:
        month = day[0] // 100
        if curr_month != month:
            avgChangePerMonth[curr_month] = sum_change / day_counter
            sum_change = 0
            curr_month = month
            day_counter = 0
        sum_change += day[2]
        day_counter = day_counter + 1
        if day == results[-1]:
            avgChangePerMonth[curr_month] = sum_change / day_counter
            sum_change = 0
            curr_month = month
            day_counter = 0
    
        
    avgCasesPerMonth = {}
    sum_change = 0
    day_counter = 0
    curr_month = 1
    for day in results:
        month = day[0] // 100
        if curr_month != month:
            avgCasesPerMonth[curr_month] = sum_change / day_counter
            sum_change = 0
            curr_month = month
            day_counter = 0
        sum_change += day[1]
        day_counter = day_counter + 1
        if day == results[-1]:
            avgCasesPerMonth[curr_month] = sum_change / day_counter
            sum_change = 0
            curr_month = month
            day_counter = 0
    
    for i in range(1,len(avgCasesPerMonth)):
        if i == 1:
            print("January: ")
        elif i == 2:
            print("February: ")
        elif i == 3:
            print("March: ")    
        elif i == 4:
            print("April: ")
        elif i == 5:
            print("May: ")
        elif i == 6:
            print("June: ")
        elif i == 7:
            print("July: ")
        elif i == 8:
            print("August: ")
        elif i == 9:
            print("September: ")
        elif i == 10:
            print("October: ")
        elif i == 11:
            print("November: ")
        elif i == 12:
            print("December: ")
        
        print("Average Cases Per Day: ")
        print(avgCasesPerMonth[i])
        print(" Average Apple Price Change Per Day: ")
        print(avgChangePerMonth[i])

if __name__ == "__main__":
    main()