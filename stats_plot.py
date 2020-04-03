#   Created by Eric Feldman
#
#   Pass 2 letter state code as a command argument  to get current COVID-19 stats
#

import matplotlib.pyplot as plt
import seaborn as sns
import requests as req
import numpy as np
from datetime import datetime
import pandas as pd
import sys

class Covid19Stats(object):

    def __init__(self, url):
        self.url = url
        self.state_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

    def getData(self, state):
        data = req.get(self.url+state)
        byLine = data.text.splitlines()
        byLine = byLine[1:]
        deaths = np.array([])
        positive = np.array([])
        date = np.array([])
        tested = np.array([])
        deathGrowth = np.array([])
        positiveGrowth = np.array([])
        for entry in byLine:
            line = entry.split(',')

            if len(line[0]) == 0:
                date = np.append(date, 0)
            else:
                date = np.append(date, datetime.fromtimestamp(int(line[0])))
            if len(line[1]) == 0:
                tested = np.append(tested, 0)
            else:
                tested = np.append(tested, line[1])
            if len(line[2]) == 0:
                positive = np.append(positive, 0)
            else:
                positive = np.append(positive, int(line[2]))
            if len(line[3]) == 0:
                deaths = np.append(deaths, 0)
            else:
                deaths = np.append(deaths, int(line[3]))
        count = 0
        for incd in deaths:
            if count == len(deaths)-1: break
            if deaths[count+1] - deaths[count] == 0:
                count+=1
                continue
            deathGrowth = np.append(deathGrowth,deaths[count+1] - deaths[count])
            count += 1
        count = 0
        for incP in positive:
            if count == len(positive)-1: break
            if positive[count+1] - positive[count] == 0:
                count += 1
                continue
            positiveGrowth = np.append(positiveGrowth,positive[count+1] - positive[count])
            count += 1
        return state, date, tested, deaths, positive, deathGrowth, positiveGrowth

    def plot(self, state, date, tested, deaths, positive, deathGrowth, positiveGrowth):
        fig, ax = plt.subplots(2,1)
        dt = pd.DataFrame({'Date':date, 'Positive':positive, 'Deaths':deaths,'Tested':tested})
        print(dt)
        # print("Positive Growth:", positiveGrowth)
        # print("Death Growth:", deathGrowth)
        ax[0].tick_params(axis='x', rotation=30)
        ax[1].tick_params(axis='x', rotation=30)
        ax[0].set_title("Tested Positive")
        ax[1].set_title("Deaths")
        sns.lineplot(x="Date", y="Positive",color='blue', data=dt, ax=ax[0])
        sns.lineplot(x="Date", y="Deaths", color='red', data=dt, ax=ax[1])
        ax[0].set(ylabel="Cases")
        ax[1].set(ylabel="Cases")
        ax[0].set(xlabel="")
        ax[1].set(xlabel="")
        plt.tight_layout()
        fig.suptitle("COVID-19 in "+state)
        fig.subplots_adjust(top=0.88)

        fig2, ax2 = plt.subplots(2)
        ax2[0].tick_params(axis='x', rotation=30)
        ax2[1].tick_params(axis='x', rotation=30)
        ax2[0].plot(date[0:len(positiveGrowth)],positiveGrowth)
        ax2[1].plot(date[0:len(deathGrowth)],deathGrowth)
        ax2[0].set_title("Delta Tested Positive")
        ax2[1].set_title("Delta Deaths")
        ax2[0].set(ylabel="Cases")
        ax2[1].set(ylabel="Cases")
        plt.tight_layout()
        fig2.subplots_adjust(top=0.88)
        fig2.suptitle("COVID-19 in " + state)
        plt.show()


# API Source:   http://coronavirusapi.com/
res = Covid19Stats("http://coronavirusapi.com/getTimeSeries/")
state, date, tested, deaths, positive, deathGrowth, positiveGrowth = res.getData(sys.argv[1])
res.plot(state, date, tested, deaths, positive, deathGrowth, positiveGrowth)

# for st in res.state_list:
#     state, date, tested, deaths, positive, deathGrowth, positiveGrowth = res.getData(st)
#     res.plot(state, date, tested, deaths, positive, deathGrowth, positiveGrowth)
