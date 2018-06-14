import numpy as np
import sqlite3 as sql
from matplotlib import pyplot as plt
from sklearn.svm import SVR
from fetch_data import fetch_data as fd
from random_dark_colors import random_dark_colors as rdc

kernel = input('Which kernel to use, polynomial or linear ([p]/l)?    ')
if len(kernel)>0 and kernel[0]=='l':
    kernel = 'linear'
else:
    kernel = 'poly'

# get players
conn = sql.connect('records.db')
c = conn.cursor()
players = list({_[0] for _ in c.execute('select player from records').fetchall()})
c.close()
conn.close()

# prepare a list of dark colors
colors = rdc(len(players))

# draw scattered plot and regression line for each player
svr = SVR(kernel=kernel, degree=2)
for i in range(len(players)):
    fps, score = fd(player=players[i])
    p = svr.fit(fps, score).predict(np.array([[_] for _ in range(20, 41)]))
    plt.scatter(fps, score, color=colors[i])
    plt.plot(np.array([[_] for _ in range(20, 41)]), p, color=colors[i], label='Player '+str(i+1))

# draw regression line for all players
fps, score = fd()
p = svr.fit(fps, score).predict(np.array([[_] for _ in range(20, 41)]))
plt.plot(np.array([[_] for _ in range(20, 41)]), p, color='black', label='all players')

# draw labels
plt.xlabel('game speed / fps')
plt.ylabel('score / points')
if kernel=='linear':
    plt.title('Support Vector Linear Regression for Facraft')
else:
    plt.title('Support Vector Polynomial Regression for Facraft')
plt.legend()

plt.show()

# draw residual plot
p = svr.fit(fps, score).predict(fps)
res = score - p
plt.plot([15, 45], [0, 0], linestyle='--', color='black', lw=1)
plt.scatter(fps, res)
plt.xlim(15, 45)

# draw labels
if kernel=='linear':
    plt.title('Residual Plot for Linear Regression')
else:
    plt.title('Residual Plot for Polynomial Regression')
plt.xlabel('fps')
plt.ylabel('residual ( $score - \widehat{score}$ )')
plt.show()

# draw residual hiostogram
plt.hist(res)

# draw labels
if kernel=='linear':
    plt.title('Histogram of Residuals for Linear Regression')
else:
    plt.title('Histogram of Residuals for Polynomial Regression')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()
