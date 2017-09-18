import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Graph:

  # Information stored for graphs:
  # Type
  # Title
  # x-axis
  # y-axis
  # x-data
  # y-data

  
  # initalize graph attributes
  def __init__(self, graphType, title, ylim, xname, yname, xdata, ydata):
    self.set_graphtype(graphType)
    self.set_title(title)
    self.set_ylim(ylim)
    self.set_xname(xname)
    self.set_yname(yname)
    self.set_xdata(xdata)
    self.set_ydata(ydata)

  # set graph type
  def set_graphtype(self, graphtype):
    if (graphtype == 'line' or graphtype == 'histogram' or graphtype == None):
      self.graphtype = graphtype
    else:
      raise Exception('Not a valid graph type.')

  # set graph title
  def set_title(self, title):
    if(isinstance(title, str)):
      self.title = title
    else:
      raise Exception('Not a valid graph title.')

  # set graph y lim
  def set_ylim(self, ylim):
    if(isinstance(ylim, float) or isinstance(ylim, int)):
      self.ylim = ylim
    else:
      raise Exception('Not a valid y limit.')

  # set graph xname
  def set_xname(self, xname):
    if(isinstance(xname, str)):
      self.xname = xname
    else:
      raise Exception('Not a valid graph x name.')

  # set graph yname
  def set_yname(self, yname):
    if(isinstance(yname, str)):
      self.yname = yname
    else:
      raise Exception('Not a valid graph y name.')

  # set graph xdata
  def set_xdata(self, xdata):
    self.xdata = xdata

  # set graph ydata
  def set_ydata(self, ydata):
    self.ydata = ydata
   
  def buildGraph(self):
    if (self.graphtype == 'line'):
      # construct line graph

      ## initialize the plot
      fig, ax = plt.subplots()
      ax.plot(self.xdata, self.ydata)
      ax.grid(True)

      if (self.ylim != None):
        ax.set_ylim(0, self.ylim)

      ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
      ax.format_ydata = self.ydata

      fig.autofmt_xdate()

      ## set axes and title
      ax.set_xlabel(self.xname)
      ax.set_ylabel(self.yname)
      ax.set_title(self.title)
      
      plt.show()

    if (self.graphtype == 'histogram'):
      plt.hist(self.ydata, bins=25, range=(10,35))
      # add the labels for the axis here
      plt.title(self.title)
      plt.show()
























