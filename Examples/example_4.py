# This example shows how to generate random numbers, fill and plot histograms, and perform a fit using ROOT
import ROOT

h_s = ROOT.TH1D("h_s", "h_s", 120, 100, 160) #new 1d histogram w/ 120 bins from 100 to 160
h_b = ROOT.TH1D("h_d", "h_d", 120, 100, 160)#same thing, but now named h_b
for i in range(100000):
    s_mgg = ROOT.gRandom.Gaus(125, 2)
    b_mgg = ROOT.gRandom.Exp(500)

    signal_weight = float(0.01)

    h_s.Fill(s_mgg, signal_weight)
    h_b.Fill(b_mgg)

c_1 = ROOT.TCanvas("canvas")#make the canvas
c_1.cd()

h_s.SetLineWidth(2)
h_s.SetLineColor(2)
h_s.SetLineStyle(1)
h_s.SetFillColor(2)

h_s.Fit("gaus","","",120,130)

max_s = h_s.GetMaximum() * 1.5

h_s.GetXaxis().SetTitle("M_{#gamma#gamma} [GeV]")
h_s.GetYaxis().SetTitle("Entries")

h_s.GetYaxis().SetRangeUser(0,max_s)

h_s.Draw()
h_b.Draw("same")

c_1.Print("plot_fit_a_gaus.png")
