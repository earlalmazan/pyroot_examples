import ROOT

def cut(input_str, sig_file_name, bkg_file_name, test_disc, train_disc, sig_disc, bkg_disc):#, test_file_name):
    inputFile = ROOT.TFile.Open(input_str)
    tree = inputFile.Get("output")
    #inputFile.Close()
    print("Preparing Data")
    PID = "flag_passedIso&&flag_passedPID"
    N_lep = "N_lep==0"
    m_nbjet_fixed80 = "m_nbjet_fixed80>0"
    N_j = "N_j>2"
    #train_disc = train_con#"(abs((1000*eta_H)%50)==26||abs((1000*eta_H)%50)==25)" #separates training from the test ones. Essentially just creates a predictable random sample selection.
    #test_disc = test_con#"(abs((1000*eta_H)%50)==22||abs((1000*eta_H)%50)==23)"
    #disc meaning discriminator

    CUT_sig_train = "&&".join([PID, N_lep, m_nbjet_fixed80, N_j, train_disc])
    CUT_bkg_train = "&&".join(["!(" + PID + ")", train_disc])
    CUT_sig_test = "&&".join([PID, N_lep, m_nbjet_fixed80, N_j, test_disc])
    CUT_bkg_test = "&&".join(["!(" + PID + ")", test_disc])

    if sig_file_name != "":
        #sig_out_file = ROOT.TFile(sig_file_name, "recreate")
        #sig_out_tree = ROOT.TTree("output_new", "output_new")
        #print("Producing Trees from Cuts")
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
