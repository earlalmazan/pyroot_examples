import ROOT

def train(sig_file, bkg_file, mdl_file, variables, methods, test_disc, train_disc, perc = [1, 1, 1, 1]):

    ROOT.TMVA.Tools.Instance()
    #choice = methods[0]

    fout = ROOT.TFile(mdl_file, "RECREATE")
    fout.cd()
    factory = ROOT.TMVA.Factory("Train", fout,
        "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification")
    dataloader = ROOT.TMVA.DataLoader("dataset")

    for element in variables:
        dataloader.AddVariable(element[0], element[1])

    # HW These are the input files
    inputS = ROOT.TFile.Open(sig_file)
    inputB = ROOT.TFile.Open(bkg_file)

    print("--- Train       : Using input file: " + str(inputS.GetName()))
    print("--- Train       : Using input file: " + str(inputB.GetName()))

    # --- Register the training and test trees

    damn_trees = ROOT.TFile.Open( "damn_trees.root", "RECREATE")

    signal   = inputS.Get("output")
    background = inputB.Get("output")
    train_con = "&&".join(train_disc)
    test_con = "&&".join(test_disc)
    sig_test = signal.CopyTree(test_con)
    sig_train = signal.CopyTree(train_con)
    bkg_test = background.CopyTree(test_con)
    bkg_train = background.CopyTree(train_con)
    #print(sig_test.GetEntries())
    #print(sig_train.GetEntries())
    #print(bkg_test.GetEntries())
    #print(bkg_train.GetEntries())

    # global event weights per tree (see below for setting event-wise weights
    signalWeight     = float(1.0)
    backgroundWeight = float(1.0)

    # You can add an arbitrary number of signal or background trees
    dataloader.AddSignalTree(sig_train, signalWeight, "Training")
    dataloader.AddSignalTree(sig_test, signalWeight, "Test")
    dataloader.AddBackgroundTree(bkg_train, backgroundWeight, "Training")
    dataloader.AddBackgroundTree(bkg_test, backgroundWeight, "Test")

    dataloader.SetBackgroundWeightExpression( "m_weight" )
    dataloader.SetSignalWeightExpression( "m_weight" )

    # HW we need to come back to these later
    # Apply additional cuts on the signal and background samples (can be different)
    mycuts = ROOT.TCut("")#"abs(var1)<0.5 && abs(var2-0.5)<1")
    mycutb = ROOT.TCut("")#"abs(var1)<0.5")

    dataloader.PrepareTrainingAndTestTree(mycuts, mycutb,
        "nTrain_Signal=" + str(sig_train.GetEntries() * perc[0]) + #str(nTrain_Signal) +
        ":nTest_Signal=" + str(sig_test.GetEntries() * perc[1]) +#+ str(nTest_Signal) +
        ":nTrain_Background=" + str(bkg_train.GetEntries() * perc[2]) +#+ str(nTrain_Background) +
        ":nTest_Background=" + str(bkg_test.GetEntries() * perc[3]) +#+ str(nTest_Background) +
        ":NormMode=NumEvents:!V")

    if "DNN_CPU" in methods:
        # General layout.
        layoutString = ROOT.TString("Layout=TANH|128,TANH|128,TANH|128,LINEAR")

        # Training strategies.
        training0 = ROOT.TString("LearningRate=1e-1,Momentum=0.6,Repetitions=1,"
            "ConvergenceSteps=10,BatchSize=512,TestRepetitions=20,"
            "WeightDecay=1e-4,Regularization=L2,"
            "DropConfig=0.0+0.5+0.5+0.5, Multithreading=True")
        training1 = ROOT.TString("LearningRate=1e-2,Momentum=0.9,Repetitions=1,"
            "ConvergenceSteps=10,BatchSize=512,TestRepetitions=10,"
            "WeightDecay=1e-4,Regularization=L2,"
            "DropConfig=0.0+0.0+0.0+0.0, Multithreading=True")
        training2 = ROOT.TString("LearningRate=1e-3,Momentum=0.1,Repetitions=1,"
            "ConvergenceSteps=10,BatchSize=512,TestRepetitions=10,"
            "WeightDecay=1e-4,Regularization=L2,"
            "DropConfig=0.0+0.0+0.0+0.0, Multithreading=True")
        trainingStrategyString = ROOT.TString("TrainingStrategy=") + training0 + "|" + training1 + "|" + training2

        # General Options.
        dnnOptions = ROOT.TString("!H:V:ErrorStrategy=CROSSENTROPY:VarTransform=N:"
            "WeightInitialization=XAVIERUNIFORM")
        dnnOptions.Append(":")
        dnnOptions.Append(layoutString)
        dnnOptions.Append(":")
        dnnOptions.Append(trainingStrategyString)

        #// Multi-core CPU implementation.
        cpuOptions = dnnOptions + ":Architecture=CPU"
        factory.BookMethod(dataloader, ROOT.TMVA.Types.kDNN, "DNN_CPU", cpuOptions)

    #// HW definition o f hyper parameters for the BDTG
    if "BDTG3" in methods: #// Gradient Boost
        factory.BookMethod( dataloader, ROOT.TMVA.Types.kBDT, "BDTG3",
                "!H:!V:NTrees=1000:MinNodeSize=7.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=3")
    if "BDT" in methods:
        factory.BookMethod( dataloader, ROOT.TMVA.Types.kBDT, "BDT",
            "!H:!V:NTrees=1000:MinNodeSize=7.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=3")

    print("Activating Training")
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    print("==> Wrote root file: " + fout.GetName())
    print("==> Train is done!")
    fout.Close()
    inputS.Close()
    inputB.Close()
    return

def view(mdl_file):
    print("==> To exit program, simply press Enter on console")
    ROOT.TMVA.TMVAGui(mdl_file)
    input()
    return
