import ROOT

def train():

    ROOT.TMVA.Tools.Instance()
    choice = ""
    while not choice in ["BDTG3", "DNN_CPU", "Quit"]:
        choice = input("\nBDTG3, DNN_CPU, or Quit:\n")
    if choice == "Quit":
        return
    print("\n")

    fout = ROOT.TFile("TMVA.root", "RECREATE")
    factory = ROOT.TMVA.Factory("Train", fout,
        "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification")
    dataloader = ROOT.TMVA.DataLoader("dataset")
    dataloader.AddVariable( "pt_H", 'F' )
    dataloader.AddVariable( "eta_H", 'F' )
    dataloader.AddVariable( "pT_hadtop1", 'F' )
    dataloader.AddVariable( "eta_hadtop1", 'F' )
    dataloader.AddVariable( "pT_hadtop2", 'F' )
    dataloader.AddVariable( "eta_hadtop2", 'F' )
    dataloader.AddVariable( "delta_eta_t1EE", 'F' )
    dataloader.AddVariable( "delta_phi_t1EE", 'F' )
    dataloader.AddVariable( "m_t1EEH", 'F' )
    dataloader.AddVariable( "m_t1EE", 'F' )


    # HW These are the input files
    inputS = ROOT.TFile.Open( "CPodd_mva_smallrange_train.root" )
    inputB = ROOT.TFile.Open( "CPeven_mva_smallrange_train.root" )

    print("--- Train       : Using input file: " + str(inputS.GetName()))
    print("--- Train       : Using input file: " + str(inputB.GetName()))

    # --- Register the training and test trees

    damn_trees = ROOT.TFile.Open( "damn_trees.root", "RECREATE")

    signal   = inputS.Get("output")
    background   = inputB.Get("output")

    # global event weights per tree (see below for setting event-wise weights
    signalWeight     = float(1.0)
    backgroundWeight = float(1.0)

    # You can add an arbitrary number of signal or background trees
    dataloader.AddSignalTree(signal, signalWeight)
    dataloader.AddBackgroundTree(background, backgroundWeight)

    dataloader.SetBackgroundWeightExpression( "m_weight" )
    dataloader.SetSignalWeightExpression( "m_weight" )

    # HW we need to come back to these later
    # Apply additional cuts on the signal and background samples (can be different)
    mycuts = ROOT.TCut("")#"abs(var1)<0.5 && abs(var2-0.5)<1")
    mycutb = ROOT.TCut("")#"abs(var1)<0.5")

    nTrain_Signal = 500
    nTrain_Background = 500

    nTest_Signal = 500
    nTest_Background = 500

    dataloader.PrepareTrainingAndTestTree(mycuts, mycutb,
        "nTrain_Signal=" + str(nTrain_Signal) +
        ":nTest_Signal=" + str(nTest_Signal) +
        ":nTrain_Background=" + str(nTrain_Background) +
        ":nTest_Background=" + str(nTest_Background) +
        ":NormMode=NumEvents:!V")

    if choice == "DNN_CPU":
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
    if choice == "BDTG3": #// Gradient Boost
        factory.BookMethod( dataloader, ROOT.TMVA.Types.kBDT, "BDTG3",
                "!H:!V:NTrees=1000:MinNodeSize=7.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=3")

    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    print("==> Wrote root file: " + fout.GetName())
    print("==> Train is done!")

    fout.Close()

    #delete factory
    #delete dataloader
    #// Launch the GUI for the root macros
    #if (!gROOT.IsBatch())
    print("==> To exit program, simply press Enter on console")
    ROOT.TMVA.TMVAGui("TMVA.root")
    input()
    return

