import ROOT
import sys

#if len(sys.argv) != 3:
#    print("Format: %s <input_file> <output_file>"%sys.argv[0])
#    sys.exit(1)
#
#inFileName = sys.argv[1]
#outFileName = sys.argv[2]
#print("Input File: " + inFileName)
#print("Output File: " + outFileName)

#This example shows how to generate random numbers, fill and plot histograms, and perform a fit using ROOT
h_s = ROOT.TH1D("h_s", "h_s", 120, 100, 160) #new 1d histogram w/ 120 bins from 100 to 160
h_b = ROOT.TH1D("h_d", "h_d", 120, 100, 160)#same thing, but now named h_b
for i in range(100000):
    s_mgg = ROOT.gRandom.Gaus(125, 2)
    b_mgg = ROOT.gRandom.Exp(500)

    signal_weight = float(0.01)

    h_s.Fill(s_mgg, signal_weight)
    h_b.Fill(b_mgg)

canvas = ROOT.TCanvas("canvas")#make the canvas
canvas.cd()#open it up
h_s.Draw("pe")#draw into it a histogram with weights taken into account
h_b.Draw("same")#draw standard histogram on same stuff
canvas.Print("plot_mass_signal_over_background.png")
#That print stuff closes it. I think...

c_1 = ROOT.TCanvas("canvas_c_1")#draw histogram with given attributes, but then just append the other one to the same template area.
c_1.cd()

h_s.SetLineWidth(2)
h_s.SetLineColor(2)
h_s.SetLineStyle(1)
h_s.SetFillColor(2)

h_b.SetLineWidth(2)
h_b.SetLineColor(1)
h_b.SetLineStyle(1)
h_b.SetFillColor(5)

max_s = float(h_s.GetMaximum() * 3)

h_s.GetXaxis().SetTitle("M_{#gamma#gamma} [GeV]")# #gamma is the gamma symbol.
h_s.GetYaxis().SetTitle("Entries")

h_s.GetYaxis().SetRangeUser(0,1.5*max_s)

h_s.Draw("pe")
h_b.Draw("same")

c_1.Print("plot_mass_signal_over_background_1.png")

c_2 = ROOT.TCanvas("canvas_c_2") #stuff 2 histograms together, then draw them together
c_2.cd()
h_s.SetLineWidth(2)
h_s.SetLineColor(2)
h_s.SetLineStyle(1)
h_s.SetFillColor(2)

h_b.SetLineWidth(2)
h_b.SetLineColor(1)
h_b.SetLineStyle(1)
h_b.SetFillColor(5)
sk = ROOT.THStack("sk", "sk")#THStack is a bunch of TH objects layered on top of each other.
sk.Add(h_b)
sk.Add(h_s)
max_b = float(h_b.GetMaximum())
sk.Draw()
sk.GetXaxis().SetTitle("M_{#gamma#gamma} [GeV]")
sk.GetYaxis().SetTitle("Entries")
c_2.Print("plot_mass_signal_over_background_2.png")

c_3 = ROOT.TCanvas("canvas_c_3")
c_3.cd()
sk_3 = ROOT. THStack("sk", "sk")
sk_3.Add(h_b)
sk_3.Add(h_s)
sk_3.Draw()
sk_3.GetXaxis().SetTitle("M_{#gamma#gamma} [GeV]")
sk_3.GetYaxis().SetTitle("Entries")

legend_3 = ROOT.TLegend(0.65, 0.8, 0.85, 0.9) #bottom left corner is at point (0.65, 0.8) and top right corner is at point (0.85, 0.9)
legend_3.AddEntry(h_s, "H #rightarrow #gamma#gamma")
legend_3.AddEntry(h_b,"Background")
legend_3.SetLineColor(0)
legend_3.SetTextSize(0.05)
legend_3.SetShadowColor(0)
legend_3.SetFillStyle(0)
legend_3.Draw("same")

cap_3 = ROOT.TLatex()
cap_3.SetNDC()
cap_3.SetTextColor(1)
cap_3.DrawText(0.2,0.25,"#int Ldt = 20.3 fb^{-1} #sqrt{s} = 8 TeV")
cap_3.DrawText(0.2,0.35,"ATLAS Internal")

c_3.Print("plot_mass_signal_over_background_3.png")
c_3.Print("plot_mass_signal_over_background_3.C")
c_3.Print("plot_mass_signal_over_background_3.eps")
