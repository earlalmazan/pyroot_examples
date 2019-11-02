import ROOT
import array
import sys

def roc_maker(sys_argv):
    bin_size = 1000
    if len(sys_argv) == 4:
        sig_bkg_file = str(sys_argv[1])
        tree_name = str(sys_argv[2])
        bdt = str(sys_argv[3])
        inFile = ROOT.TFile.Open(sig_bkg_file)
        h_sig = inFile.Get("h_sig")
        h_bkg = inFile.Get("h_bkg")
        h_sig.SetDirectory(0)
        h_bkg.SetDirectory(0)
        inFile.Close()
    elif len(sys_argv) != 5:
        print("\nFormat:\npython ROC.py <signal_file> <background_file> <tree_name> <bdt_score>\nOR\npython ROC.py <histogram_file_from_previous_run> <tree_name> <bdt_score>\n")
        sys.exit(1)
    else:
        sig_file = str(sys_argv[1])
        bkg_file = str(sys_argv[2])
        tree_name = str(sys_argv[3])
        bdt = str(sys_argv[4])

        inFile = ROOT.TFile.Open(sig_file)
        tree_obj = inFile.Get(tree_name)
        num_entries = tree_obj.GetEntries()

        conditions = []
        print("\n\n")
        while True:
            response = ""
            while not response in ["Y", "N"]:
                response = input("All Conditions Applied? Type Y or N:  ")
            if response == "Y":
                break
            user_input = []
            while True:
                user_input1 = str(input("Attribute:                    "))
                if hasattr(tree_obj, user_input1):
                    user_input.append(user_input1)
            while True:
                user_input2 = str(input("<, >, <=, >=, ==, !=, in:     "))
                if user_input2 in ["<", ">", "<=", ">=", "==", "!=", "in"]:
                    user_input.append(user_input2)
                    break
            while True:
                try:
                    user_input3 = str(input("Value:                        "))
                    user_input.append(user_input3)
                    break
                except:
                    pass
            print("\n")
            conditions.append(user_input)
        print("Opening " + str(sig_file) + " file")

        h_sig = ROOT.TH1F("h_sig", "signal", bin_size, 0, 1)
        for i in range(num_entries):
            tree_obj.GetEntry(i)
            conditions_met = True
            for condition in conditions:
                if not eval("getattr(tree_obj, '" + condition[0] + "') " +condition[1] + condition[2]):
                    conditions_met = False
                    break
            #print("successful approval")
            if conditions_met:
                #print(str(getattr(tree_obj, "weight_for_analysis")))
                h_sig.Fill(getattr(tree_obj, bdt), getattr(tree_obj, "weight_for_analysis"))
        h_sig.SetDirectory(0)
        inFile.Close()

        print("Closing " + str(sig_file) + " file")
        print("Opening " + str(bkg_file) + " file")

        inFile = ROOT.TFile.Open(bkg_file)
        tree_obj = inFile.Get(tree_name)
        num_entries = tree_obj.GetEntries()

        h_bkg = ROOT.TH1F("h_bkg", "background", bin_size, 0, 1)
        for i in range(num_entries):
            tree_obj.GetEntry(i)
            conditions_met = True
            for condition in conditions:
                if not eval("getattr(tree_obj, '" + condition[0] + "') " +condition[1] + condition[2]):
                    conditions_met = False
                    break
            if conditions_met:
                h_bkg.Fill(getattr(tree_obj, bdt), getattr(tree_obj, "weight_for_analysis"))
        h_bkg.SetDirectory(0)
        inFile.Close()

        print("Closing " + str(bkg_file) + " file.")#data collection complete.

        print("Creating " +  tree_name + "_sig_bkg.root") #store the histograms for future use.
        fOutputFile = ROOT.TFile(tree_name + "_sig_bkg.root", "recreate")
        h_sig.Write()
        h_bkg.Write()
        fOutputFile.Close()

    print("Drawing " + tree_name + "_sig_bkg.png") #draw the data for prospective watchers.

    c_tth = ROOT.TCanvas("c_tth")
    c_tth.cd()

    h_sig.SetLineWidth(2)
    h_sig.SetLineColor(2)
    h_sig.SetLineStyle(1)

    h_bkg.SetLineWidth(2)
    h_bkg.SetLineColor(3)
    h_bkg.SetLineStyle(1)

    h_sig.GetXaxis().SetTitle(bdt)
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
    c_tth.Print(tree_name + "_sig_bkg.png")

    print(tree_name + "_sig_bkg.png printed")

    print("Creating " + tree_name + "_ROC.png")
    #first, analyze the position of the highest peak.
    sig_peak = h_sig.GetXaxis().GetBinCenter(h_sig.GetMaximumBin())
    eff = array.array('d', (bin_size+1)*[0.])
    acc = array.array('d', (bin_size+1)*[0.])

    h_sig_integ = h_sig.Integral(0, bin_size+1)
    h_bkg_integ = h_bkg.Integral(0, bin_size+1)
    if sig_peak < 0.5:
        for i in range(bin_size+1):
            eff[i] = h_sig.Integral(0, i)/h_sig_integ
            acc[i] = 1 - (h_bkg.Integral(0, i)/h_bkg_integ)
    else:
        for i in range(bin_size+1):
            eff[i] = h_sig.Integral(i, bin_size)/h_sig_integ
            acc[i] = 1 - (h_bkg.Integral(i, bin_size)/h_bkg_integ)
    c_roc = ROOT.TCanvas("c_roc")
    c_roc.cd()
    graph = ROOT.TGraph(bin_size, eff, acc)
    graph.GetXaxis().SetTitle("Efficiency")
    graph.GetYaxis().SetTitle("Acceptance")
    graph.Draw("AC*")
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextColor(1)
    latex.DrawLatex(0.2, 0.25, "AUC: " + str(graph.Integral()+0.5))#round(graph.Integral()+0.5, 5)))
    c_roc.Print(tree_name + "_ROC.png")
    print(tree_name + "_ROC.png printed\n")
    print("Area Under the Curve (AUC): " + str(graph.Integral()+0.5))#round(graph.Integral()+0.5, 5)))
    print("\nComplete")

sys_argv_list = sys.argv
roc_maker(sys_argv_list)
