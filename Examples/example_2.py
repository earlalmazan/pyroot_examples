import ROOT
import array
import sys

if len(sys.argv) != 2:
    root_file = "ntuple.root"
else:
    root_file = sys.argv[1]

fOutputTree = ROOT.TTree("Hgg", "Hgg")#(tree_name, tree_title)
fOutputFile = ROOT.TFile(root_file, "recreate")

mgg = array.array('d', [0.])
weight = array.array('d', [0.])
is_signal = array.array("i", [0])
is_MC = array.array("i", [0])
n_trk = array.array("i", [0])
n_SCThits = ROOT.std.vector('double')()

fOutputTree.Branch("mgg", mgg, "mgg/D")
fOutputTree.Branch("weight", weight, "weight/D")
fOutputTree.Branch("is_signal", is_signal, "is_signal/I")
fOutputTree.Branch("is_MC", is_MC, "is_MC/I")
fOutputTree.Branch("n_SCThits", n_SCThits)

#print("Branches generated")
for i in range(100000):
    n_SCThits.clear()
    mgg[0] = ROOT.gRandom.Gaus(125, 2)
    weight[0] = 0.01
    is_signal[0] = 1
    is_MC[0] = 1

    n_trk = int(ROOT.gRandom.Poisson(25))
    for j in range(n_trk):
        n_SCThits.push_back(int(ROOT.gRandom.Poisson(14)))
    fOutputTree.Fill()
#print("100000 Entries Logged")
for i in range(150000):
    n_SCThits.clear()
    mgg[0] = ROOT.gRandom.Exp(500)
    weight[0] = 1
    is_signal[0] = 0
    is_MC[0] = 1

    n_trk = int(ROOT.gRandom.Poisson(35))
    for j in range(n_trk):
        n_SCThits.push_back(int(ROOT.gRandom.Poisson(14)))
    fOutputTree.Fill()
#print("250000 Entries Logged")

fOutputTree.Write()
#print("Written to Tree")
fOutputFile.Close()
#print("Closing File...")
