import ROOT
import sys
import array

print("Opening ntuple.root file")
f = ROOT.TFile.Open("ntuple.root")
Hgg = f.Get("Hgg")

nevt = Hgg.GetEntries()

h_s = ROOT.TH1F("h_s", "h_s", 120, 100, 160)
h_b = ROOT.TH1F("h_b", "h_b", 120, 100, 160)
s = 0
b = 0
for i in range(nevt):
    Hgg.GetEntry(i)
    if int(len(getattr(Hgg, "n_SCThits"))) <= 15:
        continue
    if getattr(Hgg, "is_signal") == 1:
        h_s.Fill(getattr(Hgg, "mgg"), getattr(Hgg, "weight"))
        #s += 1
    else:
        h_b.Fill(getattr(Hgg, "mgg"), getattr(Hgg, "weight"))
        #b += 1

h_s.SetDirectory(0)
h_b.SetDirectory(0)
#f.Close()
#print(str(s))
#print(str(b))

print("Closing ntuple.root file.")
print("Beginning Drawing")

c_1 = ROOT.TCanvas("c_1")
c_1.cd()

h_s.SetLineWidth(2)
h_s.SetLineColor(2)
h_s.SetLineStyle(1)
h_s.SetFillColor(2)

h_b.SetLineWidth(2)
h_b.SetLineColor(1)
h_b.SetLineStyle(1)
h_b.SetFillColor(5)

sk_1 = ROOT.THStack()
sk_1.Add(h_b)
sk_1.Add(h_s)
sk_1.Draw()
sk_1.GetXaxis().SetTitle("M_{#gamma#gamma} [GeV]")
sk_1.GetYaxis().SetTitle("Entries")

leg_1 = ROOT.TLegend(0.65,0.8,0.85,0.9)
leg_1.AddEntry(h_s,"H #rightarrow #gamma#gamma","FL")
leg_1.AddEntry(h_b,"Background","F")
leg_1.SetLineColor(0)
leg_1.SetTextSize(0.05)
leg_1.SetShadowColor(0)
leg_1.SetFillStyle(0)
leg_1.Draw()

cap_1 = ROOT.TLatex()
cap_1.SetNDC()
cap_1.SetTextColor(1)
cap_1.DrawLatex(0.2,0.25,"#int Ldt = 20.3 fb^{-1} #sqrt{s} = 8 TeV")
cap_1.DrawLatex(0.2,0.35,"ATLAS Internal")

c_1.Print("example3_figure_1.png")
print("Drawing completed")
