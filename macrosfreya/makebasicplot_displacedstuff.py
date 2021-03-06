import os, sys
import ROOT
##############
# example pyroot loop for histogram making on output trees of Ntupler
# January 2015 by freya.blekman@cern.ch
#

# the analysis structure see TTree/TChain description on root.cern.ch
# TChain accepts wildcards and ~infinite numbers of input files! So no need to merge files!

# very loud but useful to know what variables are stored in a tree... it prints them all
#ch.Print()

lumi=15.0
# book some histograms
outfile = ROOT.TFile("output_displaced.root","recreate")
outfile.cd()
b_elept = ROOT.TH1F("b_elept","electron p_{T}",100,0,500)
b_eleeta = ROOT.TH1F("b_eleeta","electron #eta",100,-4,4)
b_eled0 = ROOT.TH1F("b_eled0","electron |d_{0}|",200,0,2)
b_eleIso = ROOT.TH1F("b_eleIso",":electron pfIso:electrons",100,0,1)
b_eled0_zoom = ROOT.TH1F("b_eled0_zoom","electron |d_{0}|",200,0,0.2)
b_njets = ROOT.TH1F("b_njets","jet mult:jet mult:events",10,0,10)
b_jetpt = ROOT.TH1F("b_jetpt","jet p_{T}",100,0,500)
b_zpeak = ROOT.TH1F("b_zpeak","m(ee)",100,0,200)


stack_elept = ROOT.THStack("stack_elept","electron p_{T}")
#stack_elept.SetDirectory(outfile)
stack_eleeta = ROOT.THStack("stack_eleeta","electron #eta")
#stack_eleeta.SetDirectory(outfile)
stack_eleIso = ROOT.THStack("stack_eleIso","electron pfIso")
#stack_eleIso.SetDirectory(outfile)
stack_eled0 = ROOT.THStack("stack_eled0","electron d0")
#stack_eled0.SetDirectory(outfile)
stack_elenjets = ROOT.THStack("stack_elenjets","jet elelt:jet elelt:events")
#stack_njets.SetDirectory(outfile)
stack_elejetpt = ROOT.THStack("stack_elejetpt","jet p_{T}")
#stack_jetpt.SetDirectory(outfile)
stack_elezpeak = ROOT.THStack("stack_elezpeak","m(eleele)")
#stack_zpeak.SetDirectory(outfile)

names=["Wjets","Zjets","ttbar","data"]
colors=[ROOT.kGreen,ROOT.kBlue,ROOT.kRed,ROOT.kBlack]
xsecs=[20508.9,2008.4,800,-1]
filenames=["../../../datafiles/CMSSW_74X_v3-ntuples/*WJetsToLNu*.root",
           "../../../datafiles/CMSSW_74X_v3-ntuples/crab_TOPTREE-DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2-MINIAODSIM--CMSSW_74X_v3--MCRUN2_74_V9-All_*.root",
        "../../../datafiles/CMSSW_74X_v3-ntuples/crab_TOPTREE-TTJets_TuneCUETP8M1_13TeV-*.root",
        "../../../datafiles/CMSSW_74X_v3-ntuples/crab_TOPTREE-MuonEG-Run2015B-PromptReco-v1-MINIAOD--CMSSW_74X_v3--GR_P_V56-All-json_DCSONLY_Run2015B_*.root"]
skipsample=[1,1,1,1]
print xsecs
print filenames

# using lorentz vectors as easy to calculate angles, pseudorapidity, etc
lvmu=ROOT.TLorentzVector()
lve=ROOT.TLorentzVector()
lvele=ROOT.TLorentzVector()
lvjet=ROOT.TLorentzVector()


runlist=[]
#print "starting, with ", runlist.size() , " runs"

# for bookkeeping

# start of loop over events
for isam in range(len(xsecs)) :
    if skipsample[isam] ==0:
        print "skipping sample ",filenames[isam]
        continue
    bk = ROOT.TChain("startevents","startevents")
    bk.Add(filenames[isam])
    startevents=bk.GetEntries();
    ch = ROOT.TChain("tree","tree")
    ch.Add(filenames[isam])
    outfile.cd()
    h_elept=b_elept.Clone("h_elept_"+names[isam])
    h_eleeta=b_eleeta.Clone("h_eleeta_"+names[isam])
    h_eled0=b_eled0.Clone("h_eled0_"+names[isam])
    h_eled0_zoom=b_eled0_zoom.Clone("h_eled0_zoom_"+names[isam])
    h_eleIso=b_eleIso.Clone("h_eleIso_"+names[isam])
    h_elenjets=b_njets.Clone("h_elenjets_"+names[isam])
    h_elejetpt=b_jetpt.Clone("h_elejetpt_"+names[isam])
    h_elezpeak=b_zpeak.Clone("h_elezpeak"+names[isam])
    h_mupt=b_elept.Clone("h_mupt_"+names[isam])
    h_mueta=b_eleeta.Clone("h_mueta_"+names[isam])
    h_mud0=b_eled0.Clone("h_mud0_"+names[isam])
    h_mud0_zoom=b_eled0_zoom.Clone("h_mud0_zoom_"+names[isam])
    h_muIso=b_eleIso.Clone("h_muIso_"+names[isam])
    h_munjets=b_njets.Clone("h_munjets_"+names[isam])
    h_mujetpt=b_jetpt.Clone("h_mujetpt_"+names[isam])
    h_muzpeak=b_zpeak.Clone("h_muzpeak"+names[isam])
    

    
    ii=0
    nevents=ch.GetEntries()
    workxsec=xsecs[isam]
    mcweight=workxsec*lumi
    if startevents > 0 :
        mcweight/=startevents
    if workxsec == -1:
        mcweight=1  # because then it's data!
    h_elept.SetLineColor(colors[isam])
    h_eleeta.SetLineColor(colors[isam])
    h_eled0.SetLineColor(colors[isam])
    h_eled0_zoom.SetLineColor(colors[isam])
    h_eleIso.SetLineColor(colors[isam])
    h_elenjets.SetLineColor(colors[isam])
    h_elejetpt.SetLineColor(colors[isam])
    h_elezpeak.SetLineColor(colors[isam])
                                                                        
    h_mupt.SetLineColor(colors[isam])
    h_mueta.SetLineColor(colors[isam])
    h_mud0.SetLineColor(colors[isam])
    h_mud0_zoom.SetLineColor(colors[isam])
    h_muIso.SetLineColor(colors[isam])
    h_munjets.SetLineColor(colors[isam])
    h_mujetpt.SetLineColor(colors[isam])
    h_muzpeak.SetLineColor(colors[isam])

    if workxsec != -1:
        h_elept.SetFillColor(colors[isam])
        h_eleeta.SetFillColor(colors[isam])
        h_eled0.SetFillColor(colors[isam])
        h_eled0_zoom.SetFillColor(colors[isam])
        h_eleIso.SetFillColor(colors[isam])
        h_elenjets.SetFillColor(colors[isam])
        h_elejetpt.SetFillColor(colors[isam])
        h_elezpeak.SetFillColor(colors[isam])
        h_mupt.SetFillColor(colors[isam])
        h_mueta.SetFillColor(colors[isam])
        h_mud0.SetFillColor(colors[isam])
        h_mud0_zoom.SetFillColor(colors[isam])
        h_muIso.SetFillColor(colors[isam])
        h_munjets.SetFillColor(colors[isam])
        h_mujetpt.SetFillColor(colors[isam])
        h_muzpeak.SetFillColor(colors[isam])



    print "now running on sample ",filenames[isam]," with xsec:",xsecs[isam]," and lumi ",lumi, " and events: ", nevents," giving an MC weight of",mcweight," as there were ",startevents," events before skimming"
    for iev in ch:
        if ii % 10000 ==0 :
            print ii, "/", nevents
        ii+=1
# comment out the following lines if you are testing, it stops after a certain number of events
#    if ii==10000 :
#        break
        if workxsec == -1 :
            if runlist.count(iev.run_num) ==0 :
                runlist.append(iev.run_num);
        ngoodjets=0
        
        if iev.nElectrons < 1:
            continue
        if iev.nMuons < 1:
            continue
# loop over electrons - fill in lorentz vector and fill some histograms
        for iele in range(0,iev.nElectrons) :
            
            lvmu.SetPxPyPzE(iev.pX_electron[iele],iev.pY_electron[iele],iev.pZ_electron[iele],iev.E_electron[iele])
            if iele > 0 :
                lve.SetPxPyPzE(iev.pX_electron[iele-1],iev.pY_electron[iele-1],iev.pZ_electron[iele-1],iev.E_electron[iele-1])
                #                print "electron 0: ",lve.Pt()," electron 1:", lvele.Pt()
                h_elezpeak.Fill((lve+lvmu).M(),mcweight)
            h_elept.Fill(lvmu.Pt(),mcweight)
            h_eleeta.Fill(lvmu.Eta(),mcweight)
            h_eled0.Fill(abs(iev.d0_electron[iele]),mcweight)            
            h_eled0_zoom.Fill(abs(iev.d0_electron[iele]),mcweight)
            h_eleIso.Fill(iev.pfIso_electron[iele],mcweight)
        for imu in range(0,iev.nMuons) :
            
            lvmu.SetPxPyPzE(iev.pX_muon[imu],iev.pY_muon[imu],iev.pZ_muon[imu],iev.E_muon[imu])
            if imu > 0 :
                lve.SetPxPyPzE(iev.pX_muon[imu-1],iev.pY_muon[imu-1],iev.pZ_muon[imu-1],iev.E_muon[imu-1])
                #                print "muon 0: ",lve.Pt()," muon 1:", lvmu.Pt()
                h_muzpeak.Fill((lve+lvmu).M(),mcweight)
            h_mupt.Fill(lvmu.Pt(),mcweight)
            h_mueta.Fill(lvmu.Eta(),mcweight)
            h_mud0.Fill(abs(iev.d0_muon[imu]),mcweight)
            h_mud0_zoom.Fill(abs(iev.d0_muon[imu]),mcweight)
            h_muIso.Fill(iev.pfIso_muon[imu],mcweight)


                             
    #end of sample loop
    if xsecs[isam] != -1 :
        stack_elejetpt.Add(h_elejetpt)
        stack_elenjets.Add(h_elenjets)
        stack_elept.Add(h_elept)
        stack_eleeta.Add(h_eleeta)
        stack_elezpeak.Add(h_elezpeak)
    
    outfile.Write()
    print "ran over ", ii, " events"
# end of all loops
print runlist
#
## create canvas
t3=ROOT.TCanvas()
stack_elenjets.Draw()
#h_mupt_data.Draw("psame")
#
## create sub-pads and cd() to them, draw some histograms
#t3.Divide(2,2)
#t3.cd(1)
#ROOT.gPad.SetLogy()
#h_mueta.Draw()
#t3.cd(2)
#ROOT.gPad.SetLogy()
#h_mupt.Draw()
#t3.cd(3)
#ROOT.gPad.SetLogy()
#h_mud0.Draw()
#t3.cd(4)
#ROOT.gPad.SetLogy()
#h_njets.Draw()
#t3.Update()
#t3.Print("basic_muonstuff_mujetssel.gif") # TCanvas::Print also can make .pdf or .root/.C plots
#                      
