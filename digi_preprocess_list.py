import ROOT
import numpy as np
import pandas as pd

ntupla = "HiddenGluGluH_mH-375_Phi-60_ctau-1000"

def writeFiles(toFile, opt) :
   df = pd.DataFrame(data=toFile)
   event_per_file = 10000
   n_file = round(len(toFile)/event_per_file)
   dfs = [0]*n_file
   filenames = [0]*n_file
   for n in range(n_file):
      filenames[n]="./results/"+opt+"_"+ntupla+"_"+str(n)+".csv"
      if n == 0 : dfs[n]= df.iloc[:(event_per_file) ,:]
      elif n == n_file : dfs[n]= df.iloc[(n*event_per_file):,:]
      else : dfs[n]= df.iloc[((n)*event_per_file):((n+1)*event_per_file),:]
   output_files = [open(files, 'w') for files in filenames]

   for n in range(n_file):
      dfs[n].to_csv(output_files[n])

file_path = "/home/gpaggi/CMS/Ntuples/"+ntupla+".root"
#HTo2LongLivedTo4mu_MH-125_MFF-50_CTau-3000mm_noPU_noRPC.root"

nDigi = ROOT.TH1D("nDigi", "nDigi", 301, -.5, 300.5)

file = ROOT.TFile.Open(file_path)

tree = file.Get("dtNtupleProducer/DTTREE")

output = [] #[[0]*70]*4 #np.empty((4, 70), dtype=int)
output_muons = []

for i_event, event in enumerate(tree):

      if i_event % 100 == 0 :
        print("Reading event number {0}".format(i_event), end = '\r')
        
      #if i_event > 10000: break
  
      digi_list = [0]*(75*4)
      for i_digi, digi in enumerate(event.digi_station):

         if event.digi_station[i_digi] == 1: 

            digi_list[(event.digi_layer[i_digi]-1)*75+(event.digi_wire[i_digi]-1)] +=1
            
      if max(digi_list) > 0 :
         if digi_list.count(0) < (75*4) - 100:  output.append(digi_list)
         else : output_muons.append(digi_list)
         nDigi.Fill( (75*4) - digi_list.count(0) )

writeFiles(output, "shower")
writeFiles(output_muons, "muon")

filename = "histos_"+ntupla+".root"
outfile = ROOT.TFile.Open(filename, "RECREATE")
nDigi.Write()

print('\nDone')

