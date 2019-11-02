import ROOT
import array
import time

start_time = time.time()
percent_marker = 10

bin_size = 1000
print("Opening ttHr.root file")

inFile = ROOT.TFile.Open("ttHr.root")
output = inFile.Get("output")
num_entries = output.GetEntries()
modulus_marker = int((num_entries * percent_marker)//100)

h_sig = ROOT.TH1F("h_sig", "signal", bin_size, 0, 1)
for i in range(num_entries):
    output.GetEntry(i)
    if getattr(output, "m_njet") >= 3 and getattr(output, "m_nbjet_fixed80") > 0 and getattr(output, "m_nlep") == 0:
        h_sig.Fill(getattr(output, "m_score_wisc"))
    #if i%modulus_marker == 0:
    #    print(str(int((i*100)/num_entries)) + "% complete")
h_sig.SetDirectory(0)
inFile.Close()

print("Closing ttHr.root file")
print("Opening datar.root file")

inFile = ROOT.TFile.Open("datar.root")
output = inFile.Get("output")
num_entries = output.GetEntries()
modulus_marker = int((num_entries * percent_marker)//100)

h_bkg = ROOT.TH1F("h_bkg", "background", bin_size, 0, 1)
for i in range(num_entries):
    output.GetEntry(i)
    if getattr(output, "m_njet") >= 3 and getattr(output, "m_nbjet_fixed80") > 0 and getattr(output, "m_nlep") == 0:
        h_bkg.Fill(getattr(output, "m_score_wisc"))
    #if i%modulus_marker == 0:
    #    print(str(int((i*100)/num_entries)) + "% complete")
h_bkg.SetDirectory(0)
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
print("Closing datar.root file.")
print("Drawing ttH_sig_bkg.png")

c_tth = ROOT.TCanvas("c_tth")
c_tth.cd()

h_sig.SetLineWidth(2)
h_sig.SetLineColor(2)
h_sig.SetLineStyle(1)

h_bkg.SetLineWidth(2)
h_bkg.SetLineColor(3)
h_bkg.SetLineStyle(1)

h_sig.GetXaxis().SetTitle("m_score_wisc")
h_sig.GetYaxis().SetTitle("Entries")

legend_3 = ROOT.TLegend(0.65, 0.6, 0.85, 0.7) #bottom left corner is at point (0.65, 0.8) and top right corner is at point (0.85, 0.9)
legend_3.AddEntry(h_sig, "Signal")
legend_3.AddEntry(h_bkg,"Background")
legend_3.SetLineColor(0)
legend_3.SetTextSize(0.05)
legend_3.SetShadowColor(0)
legend_3.SetFillStyle(0)

h_sig.Draw()
h_bkg.Draw("same")
legend_3.Draw("same")
c_tth.Print("ttH_sig_bkg.png")

print("ttH_sig_bkg.png printed")
print("Creating ROC")

eff = array.array('d', (bin_size)*[0.])
acc = array.array('d', (bin_size)*[0.])

h_sig_integ = h_sig.Integral(1, bin_size)
h_bkg_integ = h_bkg.Integral(1, bin_size)
for i in range(bin_size):
    eff[i] = h_sig.Integral(1, i+1)/h_sig_integ
    acc[i] = 1 - (h_bkg.Integral(1, i+1)/h_bkg_integ)
    #print(str(eff[i]) + ", " + str(acc[i]))
c_roc = ROOT.TCanvas("c_roc")
c_roc.cd()
graph = ROOT.TGraph(bin_size-2, eff, acc)
graph.GetXaxis().SetTitle("Efficiency")
graph.GetYaxis().SetTitle("Acceptance")
graph.Draw("AC*")
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextColor(1)
latex.DrawLatex(0.2, 0.25, "AUC: " + str(graph.Integral()+0.5))
c_roc.Print("ttH_ROC.png")
print("ttH_ROC.png printed\n")
print("Area Under the Curve (AUC): " + str(graph.Integral()+0.5))
print("\nComplete")
