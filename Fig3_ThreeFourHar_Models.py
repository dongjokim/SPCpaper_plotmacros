import numpy as np
import ROOT

import scipy
from scipy import interpolate

import sys
sys.path.append("JPyPlotRatio");


import JPyPlotRatio

f = ROOT.TFile("data/Output_ALICE.root","read");
fmodel = ROOT.TFile("data/Output_TrentoVISHNU.root","read");

obsPanel = [0,1,2,3,4];
obsTypeStr  = [
		"2Psi2_3Psi3_n5Psi5","8Psi2_n3Psi3_n5Psi5","2Psi2_n6Psi3_4Psi4","2Psi2_4Psi4_n6Psi6",
		"2Psi2_n3Psi3_n4Psi4_5Psi5"
		];
plabel     = [
	      "$\\langle cos[2\\Psi_{2}+3\\Psi_{3}-5\\Psi_{5}]\\rangle$",
	      "$\\langle cos[8\\Psi_{2}-3\\Psi_{3}-5\\Psi_{5}]\\rangle$",
	      "$\\langle cos[2\\Psi_{2}-6\\Psi_{3}+4\\Psi_{4}]\\rangle$",
	      "$\\langle cos[2\\Psi_{2}+4\\Psi_{4}-6\\Psi_{6}]\\rangle$", # 3 har
	      "$\\langle cos[2\\Psi_{2}-3\\Psi_{3}-4\\Psi_{4}+5\\Psi_{5}]\\rangle$", # 4 har
	      "" # epmty for dummy pad
	      ];
dataTypeStr = ["ALICE","{T\\raisebox{-.5ex}{R}ENTo} (cumulants)","{T\\raisebox{-.5ex}{R}ENTo} (eccentricities)","{T\\raisebox{-.5ex}{R}ENTo} + VISH2+1 + UrQMD"];
dataTypeInRoot = ["ALICE","_Trento_Cumulants","_Trento_Ecc","_TrentoVISHNU_FinalState"];
dataTypePlotParams = [
        {'plotType':'data','color':'red','fmt':'o','markersize':5.0},
        {'plotType':'data','color':'#e580ff','fmt':'X','fillstyle':'none','markersize':5.5},
        {'plotType':'data','color':'#44aa11','fmt':'h','markersize':4.0},
        {'plotType':'data','color':'red','fmt':'D','fillstyle':'none','markersize':5.0},
        {'plotType':'data','color':'cyan','fmt':'d','fillstyle':'none','markersize':5.5}
];
modelTypePlotParams = [
#	{'plotType':'theory','facecolor':'C0','edgecolor':'C0','alpha':0.5,'linestyle':'solid','linecolor':'C0'},
#	{'plotType':'theory','facecolor':'C1','edgecolor':'C1','alpha':0.5,'linestyle':'dashed','linecolor':'C1'},
#	{'plotType':'theory','facecolor':'C2','edgecolor':'C2','alpha':0.5,'linestyle':'dotted','linecolor':'C2'},
	{'plotType':'theory','color':'#0051a2','alpha':0.5,'linestyle':'dashed'},
	{'plotType':'theory','color':'#0051a2','alpha':0.5,'linestyle':'dotted'},
	{'plotType':'theory','color':'red','alpha':0.5,'linestyle':'solid'}
];
def RemovePoints(arrays, pointIndices):
	return tuple([np.delete(a,pointIndices) for a in arrays]);

# define panel/xaxis limits/titles
ny = 3;
nx = 2;
xlimits = [(0.,53.)];
ylimits = [(-0.6,0.85),(-0.15,0.17),(-0.15,0.5),(-0.15,0.15),(-0.55,0.85),(-0.15,0.5)];

xtitle = ["Centrality percentile"];
ytitle = ["Correlations","Correlations"];
ytitleRight = ["Correlations"];
# Following two must be added
toptitle = "PbPb $\\sqrt{s_{NN}}$ = 2.76 TeV"; # need to add on the top
dataDetail = "$0.2 < p_\\mathrm{T} < 5.0\\,\\mathrm{GeV}/c$\n$|\\eta| < 0.8$";

plot = JPyPlotRatio.JPyPlotRatio(panels=(ny,nx),panelsize=(5,5),disableRatio=[0,1,2],
	rowBounds=ylimits, #only one row, add the shared ylims
	colBounds={0:xlimits[0],1:xlimits[0]}, #two columns, set xlimit for both of them
	ratioBounds={0:(-1,3),1:(-1,3)},
	panelPrivateScale=[1,3],
	#panelLabel={i:label for i,label in enumerate(plabel)},
	panelLabelLoc=(0.09,0.86),panelLabelSize=11,
	panelLabel=plabel,
	#panelScaling={3:5},
	panelLabelAlign="left",
legendPanel=5,legendLoc=(0.60,0.36),legendSize=9,ylabel={0:ytitle[0],1:ytitle[0],2:ytitle[0]});
plot.GetPlot().text(0.5,0.05,xtitle[0],size=plot.axisLabelSize,horizontalalignment="center");
plot.GetAxes(1).yaxis.tick_right();
plot.GetAxes(3).yaxis.tick_right();
#plot.GetAxes(5).yaxis.tick_right();

plot.EnableLatex(True);

#plot.EnableLatex(True);
obsN = len(obsTypeStr);
print(obsN)

#scale1 = {4:10,5:10};

plot.GetAxes(0).plot([0,50],[0,0],linestyle=":",color="gray");
plot.GetAxes(1).plot([0,50],[0,0],linestyle=":",color="gray");
plot.GetAxes(2).plot([0,50],[0,0],linestyle=":",color="gray");
plot.GetAxes(3).plot([0,50],[0,0],linestyle=":",color="gray");
plot.GetAxes(4).plot([0,50],[0,0],linestyle=":",color="gray");



for i in range(0,obsN):
	gr = f.Get("{:s}{:s}".format(obsTypeStr[i],"_Stat"));
	plot1 = plot.AddTGraph(obsPanel[i],gr,**dataTypePlotParams[0]);
	if(i==0):
		plot1 = plot.AddTGraph(obsPanel[i],gr,**dataTypePlotParams[0],label=dataTypeStr[0]);
	# systematics
	grsyst = f.Get("{:s}{:s}".format(obsTypeStr[i],"_Syst"));
	_,_,_,yerrsyst = JPyPlotRatio.TGraphErrorsToNumpy(grsyst);
	plot.AddSyst(plot1,yerrsyst);
	# model
	for j in range(0,3):
		if(i==1 and j==2):
			break
		grmodel = fmodel.Get("{:s}{:s}".format(obsTypeStr[i],dataTypeInRoot[j+1]));
		#print("{:s}{:s}".format(obsTypeStr[i],dataTypeInRoot[j+1]))
		#print(j)
		plotModel = plot.AddTGraph(obsPanel[i],grmodel,**modelTypePlotParams[j],label=dataTypeStr[j+1]);

f.Close();
print("I am here,,")
#plot.GetPlot().text(0.16,0.31,"ALICE",fontsize=9);
plot.GetPlot().text(0.64,0.28,toptitle,fontsize=9);
plot.GetPlot().text(0.64,0.25,dataDetail,fontsize=9);
#plot.GetAxes(3).text(0.1,0.1,dataDetail,fontsize=9);

plot.Plot();

#plot.GetRatioAxes(3).remove();

plot.Save("figs/Fig3_ThreeFourHar_models.pdf");
plot.Show();

