import ROOT
import sys
import array
import time

print("Opening ttHr.root file")
inFile = ROOT.TFile.Open("ttHr.root")
output = inFile.Get("output")

num_entries = output.GetEntries()
percent_marker = 5 #percent
modulus_marker = int((num_entries * percent_marker)//100)
h_pt = ROOT.TH1F("h_pt", "jet0_pt_1", 750, 0, 750)
h_t1 = ROOT.TH1F("h_t1", "t1_score", 750, 0.7, 1.1)
start_time = time.time()
for i in range(num_entries):
    output.GetEntry(i)
    if getattr(output, "m_njet") >= 3 and getattr(output, "m_nbjet_fixed80") > 0 and getattr(output, "m_nlep") == 0:
        h_pt.Fill(getattr(output, "jet0_pt_1"))
        h_t1.Fill(getattr(output, "t1_score"))
    if i%modulus_marker == 0:
        print(str(int((i*100)/num_entries)) + "% complete")

h_pt.SetDirectory(0)
h_t1.SetDirectory(0)
inFile.Close()

time_msg = "Total Time Elapsed: "
diff_time = int(time.time()-start_time)
seconds = diff_time % 60
minutes = 0
if seconds != diff_time:
    minutes = int((diff_time - seconds)//60)
    time_msg += str(minutes) + " minutes and "
time_msg += str(seconds) + " seconds."

print("100% complete")
print(time_msg)
print("Closing ttHr.root file.")
print("Drawing ttH_pt.png")

c_pt = ROOT.TCanvas("c_pt")
c_pt.cd()

h_pt.SetLineWidth(2)
h_pt.SetLineColor(2)
h_pt.SetLineStyle(1)
h_pt.SetFillColor(2)

h_pt.GetXaxis().SetTitle("pt_value")
h_pt.GetYaxis().SetTitle("Entries")

h_pt.Draw()
c_pt.Print("ttH_pt.png")

print("Drawing ttH_pt.png completed")
print("Drawing ttH_t1.png")

c_t1 = ROOT.TCanvas("c_t1")
c_t1.cd()

h_t1.SetLineWidth(2)
h_t1.SetLineColor(2)
h_t1.SetLineStyle(1)
h_t1.SetFillColor(2)

h_t1.GetXaxis().SetTitle("t1_value")
h_t1.GetYaxis().SetTitle("Entries")

h_t1.Draw()
c_t1.Print("ttH_t1.png")

print("Drawing ttH_t1.png completed")
print("Complete")
