import numpy as np
import ROOT

import scipy
from scipy import interpolate

import sys
sys.path.append("JPyPlotRatio");


import JPyPlotRatio

f = ROOT.TFile("data/Output_ALICE.root","read");
fmodel = ROOT.TFile("data/Output_TrentoVISHNU.root","read");

obsPanel = [0,0,0,0,1,1,1,1,1];
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
dataTypeStr = ["ALICE","{T\\raisebox{-.5ex}{R}ENTo} (cumulants)","{T\\raisebox{-.5ex}{R}ENTo} (eccentricities)","{T\\raisebox{-.5ex}{R}ENTo} + VISH2+1 + UrQMD"];
dataTypeInRoot = ["ALICE","_Trento_Cumulants","_Trento_Ecc","_TrentoVISHNU_FinalState"];
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

modelDraw = 0
imodel = 3; # based on dataTypeStr  and dataTypeInRoot
# define panel/xaxis limits/titles
ny = 1;
nx = 2;
xlimits = [(-1.,52.)];
ylimits = [(-0.4,0.6)];

xtitle = ["Centrality percentile"];
ytitle = ["Correlations"];
ytitleRight = ["NSC(k,l,m)"];
# Following two must be added
toptitle = "PbPb $\\sqrt{s_{NN}}$ = 2.76 TeV"; # need to add on the top
dataDetail = "$0.2 < p_\\mathrm{T} < 5.0\\,\\mathrm{GeV}/c$\n$|\\eta| < 0.8$";

plot = JPyPlotRatio.JPyPlotRatio(panels=(ny,nx),panelsize=(5,6),disableRatio=[0],
	rowBounds=ylimits, #only one row, add the shared ylims
	colBounds={0:xlimits[0],1:xlimits[0]}, #two columns, set xlimit for both of them
	ratioBounds={0:(-1,3),1:(-1,3)},
	#panelPrivateScale=[1,3,5],
	#panelLabel={i:label for i,label in enumerate(plabel)},
	panelLabelLoc=(0.07,0.86),panelLabelSize=9,
	#panelScaling={3:5},
	panelLabelAlign="left",
	systPatchWidth = 0.03,
	legendPanel={0:0,1:1},legendLoc={0:(0.65,0.20),1:(0.35,0.18)},legendSize=9,xlabel=xtitle[0],ylabel=ytitle[0]);

plot.GetAxes(1).yaxis.tick_right();

plot.EnableLatex(True);

#plot.EnableLatex(True);
obsN = len(obsTypeStr);
datN = len(dataTypeStr);

#scale1 = {4:10,5:10};

plot.GetAxes(0).plot([0,50],[0,0],linestyle=":",color="gray");
plot.GetAxes(1).plot([0,50],[0,0],linestyle=":",color="gray");

for i in range(0,obsN):
	gr = f.Get("{:s}{:s}".format(obsTypeStr[i],"_Stat"));
	x,y,_,yerr = JPyPlotRatio.TGraphErrorsToNumpy(gr);
	if(i==5 or i==8):
		x = x[1:] 
		y = y[1:]
		yerr = yerr[1:]
	if(modelDraw == 0):			
		plot1 = plot.Add(obsPanel[i],(x,y,yerr),**dataTypePlotParams[i],label=plabel[i],labelLegendId=obsPanel[i]);
		# systematics
		grsyst = f.Get("{:s}{:s}".format(obsTypeStr[i],"_Syst"));
		_,_,_,yerrsyst = JPyPlotRatio.TGraphErrorsToNumpy(grsyst);
		if(i==5 or i==8):
			yerrsyst = yerrsyst[1:]
		plot.AddSyst(plot1,yerrsyst);
	if(modelDraw == 1 and i!=5):
			# model
		grmodel = fmodel.Get("{:s}{:s}".format(obsTypeStr[i],dataTypeInRoot[imodel]));
		plotModel = plot.Add(obsPanel[i],grmodel,**dataTypePlotParams[i],label=plabel[i],labelLegendId=obsPanel[i]);

f.Close();



#plot.GetRatioAxes(3).remove();

if(modelDraw==0):
	plot.GetPlot().text(0.15,0.81,"ALICE",fontsize=9);
	plot.GetPlot().text(0.15,0.77,toptitle,fontsize=9);
	plot.GetPlot().text(0.16,0.25,dataDetail,fontsize=9);
	#plot.GetAxes(3).text(0.1,0.1,dataDetail,fontsize=9);
	plot.Plot();
	plot.Save("figs/Fig1_AllObs.pdf");
if(modelDraw==1):
	plot.GetPlot().text(0.15,0.81,dataTypeStr[imodel],fontsize=9);
	plot.GetPlot().text(0.15,0.77,toptitle,fontsize=9);
	plot.GetPlot().text(0.16,0.25,dataDetail,fontsize=9);
	#plot.GetAxes(3).text(0.1,0.1,dataDetail,fontsize=9);
	plot.Plot();
	plot.Save("figs/Fig1_AllObs_{:s}.pdf".format(dataTypeInRoot[imodel]));
plot.Show();

