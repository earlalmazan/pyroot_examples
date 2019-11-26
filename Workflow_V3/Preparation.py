import ROOT
import array

def calculate(input_str, event_type, event_attr):
    input_file = ROOT.TFile.Open(input_str)
    input_tree = input_file.Get("output")

    prefix = input_str[:int(input_str.find("."))]
    output_file = ROOT.TFile(prefix + "c.root", "recreate")
    output_file.cd()
    output_tree = input_tree.CloneTree(0)

    if event_type == "tH":
        event1 = event_attr + "_t1H"
        event2 = event_attr + "_t2H"
        sumv_value1 = array.array('d', [0.])
        sumv_value2 = array.array('d', [0.])
        output_tree.Branch(event1, sumv_value1, event1 + "/D")
        output_tree.Branch(event2, sumv_value2, event2 + "/D")
    else:
        event = event_attr + "_" + event_type
        sumv_value = array.array('d', [0.])
        output_tree.Branch(event, sumv_value, event + "/D")

    print("Calculating " + event)
    for i in  range(input_tree.GetEntries()):
        if i%5000 == 0:
            print("--- ... Processing event: " + str(i))
        input_tree.GetEntry(i)
        t1 = ROOT.Math.PtEtaPhiMVector(getattr(input_tree, "m_top_pt")[0], getattr(input_tree, "m_top_eta")[0], getattr(input_tree, "m_top_phi")[0], getattr(input_tree, 'm_top_m')[0])
        t2 = ROOT.Math.PtEtaPhiMVector(getattr(input_tree, "m_top_pt")[1], getattr(input_tree, "m_top_eta")[1], getattr(input_tree, "m_top_phi")[1], getattr(input_tree, 'm_top_m')[1])
        H = ROOT.Math.PtEtaPhiMVector(getattr(input_tree, "m_H_pt")[0], getattr(input_tree, "m_H_eta")[0], getattr(input_tree, "m_H_phi")[0], getattr(input_tree, 'm_H_m')[0])
        if event_type == "tH":
            sumv_1 = t1 + H
            sumv_2 = t2 + H

            if event_attr == "m":
                sumv_value = [sumv_1.M(), sumv_2.M()]
            elif event_attr == "eta":
                sumv_value = [sumv_1.Eta(), sumv_2.Eta()]
            elif event_attr == "pt":
                sumv_value = [sumv_1.Pt(), sumv_2.Pt()]

            if sumv_value[0] > sumv_value[1]:
                sumv_value1 = sumv_value[0]
                sumv_value2 = sumv_value[1]

        else:
            if event_type == "ttH":
                sumv = t1 + t2 + H
            elif event_type == "tt":
                sumv = t1 + t2

            if event_attr == "m":
                sumv_value[0] = sumv.M()
            elif event_attr == "eta":
                sumv_value[0] = sumv.Eta()
            elif event_attr == "pt":
                sumv_value[0] = sumv.Pt()
        output_tree.Fill()
    print("Calculations Complete.")
    output_file.cd()
    output_tree.Write()
    return


def cut(input_str, sig_file_name, bkg_file_name, test_disc, train_disc, sig_disc, bkg_disc):#, test_file_name):
    inputFile = ROOT.TFile.Open(input_str)
    tree = inputFile.Get("output")
    print("Preparing Data")

    CUT_sig_train = "&&".join(sig_disc + train_disc)
    CUT_bkg_train = "&&".join(bkg_disc + train_disc)
    CUT_sig_test = "&&".join(sig_disc + test_disc)
    CUT_bkg_test = "&&".join(bkg_disc + test_disc)

    if sig_file_name != "":
        print("Creating Signal File: " + sig_file_name)
        sig_out_file = ROOT.TFile(sig_file_name, "recreate")

        print("Cutting Primary Tree into Sig_Train and Sig_Test")
        sig_train_tree = tree.CopyTree(CUT_sig_train)
        sig_test_tree = tree.CopyTree(CUT_sig_test)

        print("# of Entries in Sig_Train: " + str(sig_train_tree.GetEntries()))
        print("# of Entries in Sig_Test: " + str(sig_test_tree.GetEntries()))

        print("Loading Signal Trees to Primary Signal Tree")
        sig_list = ROOT.TList()
        sig_list.Add(sig_train_tree)
        sig_list.Add(sig_test_tree)
        sig_out_tree = ROOT.TTree.MergeTrees(sig_list)
        sig_out_tree.Write()
        sig_out_file.Close()

    if bkg_file_name != "":
        print("Creating Background File: " + bkg_file_name)
        bkg_out_file = ROOT.TFile(bkg_file_name, "recreate")

        print("Cutting Primary Tree into Bkg_Train and Bkg_Test")
        bkg_train_tree = tree.CopyTree(CUT_bkg_train)
        bkg_test_tree = tree.CopyTree(CUT_bkg_test)

        print("# of Entries in Bkg_Train: " + str(bkg_train_tree.GetEntries()))
        print("# of Entries in Bkg_Test: " + str(bkg_test_tree.GetEntries()))

        print("Loading Background Tress to Primary Background Tree")
        bkg_list = ROOT.TList()
        bkg_list.Add(bkg_train_tree)
        bkg_list.Add(bkg_test_tree)
        bkg_out_tree = ROOT.TTree.MergeTrees(bkg_list)
        bkg_out_tree.Write()
        bkg_out_file.Close()
    inputFile.Close()
    return
