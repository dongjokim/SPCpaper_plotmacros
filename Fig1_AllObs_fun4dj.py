import numpy as np
import ROOT

import scipy
from scipy import interpolate

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sys
sys.path.append("JPyPlotRatio");

from matplotlib.lines import Line2D


import JPyPlotRatio

f = ROOT.TFile("data/Output_ALICE.root","read");

obsTypeStr  = ["4Psi4_n4Psi2","6Psi3_n6Psi2","6Psi6_n6Psi2","6Psi6_n6Psi3",
		"2Psi2_3Psi3_n5Psi5","8Psi2_n3Psi3_n5Psi5","2Psi2_n6Psi3_4Psi4","2Psi2_4Psi4_n6Psi6",
		"2Psi2_n3Psi3_n4Psi4_5Psi5"
		];
plabel     = ["$\\langle cos[4(\\Psi_{4}-\\Psi_{2})]\\rangle$",
	      "$\\langle cos[6(\\Psi_{2}-\\Psi_{3})]\\rangle$",
	      "$\\langle cos[6(\\Psi_{6}-\\Psi_{2})]\\rangle$",
	      "$\\langle cos[6(\\Psi_{6}-\\Psi_{3})]\\rangle$", # 2 har
	      "$\\langle cos[2\\Psi_{2}+3\\Psi_{3}-5\\Psi_{5}]\\rangle$",
	      "$\\langle cos[8\\Psi_{2}-3\\Psi_{3}-5\\Psi_{5}]\\rangle$",
	      "$\\langle cos[2\\Psi_{2}-6\\Psi_{3}+4\\Psi_{4}]\\rangle$",
	      "$\\langle cos[2\\Psi_{2}+4\\Psi_{4}-6\\Psi_{6}]\\rangle$", # 3 har
	      "$\\langle cos[2\\Psi_{2}-3\\Psi_{3}-4\\Psi_{4}+5\\Psi_{5}]\\rangle$" # 4 har
	      ];

dataTypePlotParams = [
        {'plotType':'data','color':'black','fmt':'o','markersize':5.5},
        {'plotType':'data','color':'#0051a2','fmt':'d','fillstyle':'none','markersize':6.0},
        {'plotType':'data','color':'blue','fmt':'D','fillstyle':'none','markersize':5.5},
        {'plotType':'data','color':'red','fmt':'s','markersize':5.5},# 2 har
        {'plotType':'data','color':'#660080','fmt':'*','fillstyle':'none','markersize':6.0},
        {'plotType':'data','color':'#9955ff','fmt':'d','markersize':6.0},
        {'plotType':'data','color':'m','fmt':'X','fillstyle':'none','markersize':5.5},
        {'plotType':'data','color':'seagreen','fmt':'h','markersize':5.5},
        {'plotType':'data','color':'red','fmt':'H','fillstyle':'none','markersize':5.5}
];


def RemovePoints(arrays, pointIndices):
	return tuple([np.delete(a,pointIndices) for a in arrays]);


xlimits = [(-1.,52.)];
ylimits = [(-0.3,0.55)];

xtitle = ["Centrality percentile"];
ytitle = ["Correlations"];
ytitleRight = ["NSC(k,l,m)"];
# Following two must be added
toptitle = "PbPb $\\sqrt{s_{NN}}$ = 2.76 TeV"; # need to add on the top
dataDetail = "$0.2 < p_\\mathrm{T} < 5.0\\,\\mathrm{GeV}/c$\n$|\\eta| < 0.8$";
plables = [ "(a)", "(b)" ];



#plot.EnableLatex(True);
obsN = len(obsTypeStr);

df = pd.DataFrame();
gr = f.Get("{:s}{:s}".format(obsTypeStr[0],"_Stat"));
x,y,_,yerr = JPyPlotRatio.TGraphErrorsToNumpy(gr);
df['Centrality'] = x.tolist()
df_cols = ['ObsType','Observables', 'Centrality' , 'Correlation']
df_new = pd.DataFrame(columns=df_cols)

for i in range(0,obsN):
	gr = f.Get("{:s}{:s}".format(obsTypeStr[i],"_Stat"));
	x,y,_,yerr = JPyPlotRatio.TGraphErrorsToNumpy(gr);
	for ic in range(0,len(x)):
		#new_row =[obsTypeStr[i], x[i] ,y[i]]
		df_new = df_new.append({'ObsType': "SPC",'Observables': obsTypeStr[i], 'Centrality': x[i], 'Correlation': y[i]}, ignore_index=True) # yuck
	df[obsTypeStr[i]] = y.tolist()
	
f.Close();

print(df)
print(df_new)
for i in range(0,obsN):
	g = sns.scatterplot(data=df, x="Centrality", y=obsTypeStr[i], size=obsTypeStr[i], legend=False, sizes=(20, 400))
	#sns.relplot(data=df, x="Centrality", y=obsTypeStr[i], size=obsTypeStr[i], legend=False, sizes=(20, 200))
plt.legend(plabel, loc='upper left',fontsize='x-small',title_fontsize='4')
# Set x-axis label
plt.xlabel(xtitle[0])
# Set y-axis label
plt.ylabel(ytitle[0])
g.set(xlim=(-1,60),ylim=(-0.1,1))
# show the graph
plt.show()



