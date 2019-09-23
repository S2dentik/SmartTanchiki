import matplotlib.pyplot as plt
from datetime import datetime
import os

class Statistics():
  def __init__(self):
    self.results = []
    self.currentProgress = 0
    self.folderName = 'statistics'

  def increment(self):
    self.currentProgress += 1

  def commit(self):
    self.results.append(self.currentProgress)
    self.currentProgress = 0

  def save(self):
    dt = datetime.now()


    plt.plot(self.results)
    plt.xlabel('Game No.')
    plt.ylabel('Score')

    dtPlotTitle = dt.strftime("%d/%m/%Y %H:%M:%S")
    plt.title(f"DQN {dtPlotTitle}")

    if not os.path.exists(self.folderName):
      os.mkdir(self.folderName)

    dtFileName = dt.strftime("%d-%m-%Y_%H-%M-%S")
    plt.savefig(f"{self.folderName}/progress-{dtFileName}.png")
  