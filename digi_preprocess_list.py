import ROOT
import numpy as np
import pandas as pd

ntupla = "HiddenGluGluH_mH-125_Phi-30_ctau-500"



def writeFiles(toFile, opt) :

   names = []
   for c in range(n_chann) :
      for l in range(8) :
         names.append(f'ch{c+1}l{l+1}')
   names.append('wh')
   names.append('st')

   df = pd.DataFrame(data=toFile, columns =names)

   event_per_file = 5000
   n_file = round(len(toFile)/event_per_file)
   dfs = [0]*n_file
   filenames = [0]*n_file
   for n in range(n_file):
      filenames[n]="./results/"+ntupla+"/"+opt+"_"+ntupla+"_"+str(n)+".csv"
      if n == 0 : dfs[n]= df.iloc[:(event_per_file) ,:]
      elif n == n_file : dfs[n]= df.iloc[(n*event_per_file):,:]
      else : dfs[n]= df.iloc[((n)*event_per_file):((n+1)*event_per_file),:]
   output_files = [open(files, 'w') for files in filenames]

   for n in range(n_file):
      dfs[n].to_csv(output_files[n])

file_path = "/home/gpaggi/CMS/Ntuples/"+ntupla+".root"
#HTo2LongLivedTo4mu_MH-125_MFF-50_CTau-3000mm_noPU_noRPC.root"



nDigi = [[ROOT.TH1D(f"nDigi_wh{wh}_st{st}", f"nDigi_wh{wh}_st{st}", 151, -.5, 150.5) for st in range(1, 5)] for wh in range(-2, 3)]

file = ROOT.TFile.Open(file_path)

tree = file.Get("dtNtupleProducer/DTTREE")

output = [] #[[0]*70]*4 #np.empty((4, 70), dtype=int)
output_muons = []
n_chann = 98
dimension = (n_chann*8)

shower_cut = 20

for i_event, event in enumerate(tree):

      if i_event % 100 == 0 :
        print("Reading event number {0}".format(i_event), end = '\r')
        
      #if i_event > 10000: break

      digi_list = [[[0]*(dimension+2) for i in range(4)] for i in range(5)] # [ wheel ] [ station ] [ canali * 8 layers] + 2 per wheel station evento
      for i_digi, digi in enumerate(event.digi_station):

         wh = event.digi_wheel[i_digi]
         st = event.digi_station[i_digi]
         
         #skip mb1 external wheels -> higher bkg
         if  st == 1 and abs(wh) == 2: continue

         # skip layer theta
         if event.digi_superLayer[i_digi] == 2 : continue

         Sl = 0 if (event.digi_superLayer[i_digi] == 1 ) else 1
         #print(f'evento in wh {event.digi_wheel[i_digi]} sl {event.digi_superLayer[i_digi]} layer {event.digi_layer[i_digi]} wire {event.digi_wire[i_digi]} lo sto mettendo in list [{event.digi_wheel[i_digi]+2}] [{((event.digi_layer[i_digi]-1)+(4*Sl))*90+(event.digi_wire[i_digi]-1)}]')
         digi_list[wh+2] [ st-1] [ ( (event.digi_layer[i_digi]-1) + (4*Sl) )*n_chann + (event.digi_wire[i_digi]-1) ] += 1
         digi_list[wh+2] [ st-1] [ len(digi_list[wh+2] [ st-1]) - 2] = wh
         digi_list[wh+2] [ st-1] [ len(digi_list[wh+2] [ st-1]) - 1] = st
         
      for wh in range(5):
         for st in range(4):
            Max = max(digi_list[wh][st][:dimension])
            if Max > 0: 
               if digi_list[wh][st].count(0) < (dimension - shower_cut):  output.append(digi_list[wh][st])
               else : output_muons.append(digi_list[wh][st])
               nDigi[wh][st].Fill( dimension - digi_list[wh][st].count(0) )

writeFiles(output, "shower")
writeFiles(output_muons, "muon")

filename = "histos_"+ntupla+".root"
outfile = ROOT.TFile.Open(filename, "RECREATE")
for wh in range(5):
   for st in range(4):
      nDigi[wh][st].Write()

print('\nDone')

