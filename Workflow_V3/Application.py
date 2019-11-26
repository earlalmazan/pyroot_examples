import ROOT, array

def apply(test_file, variables, methods, variant): #inputName = mdl_file = file for the model
    ROOT.TMVA.Tools.Instance() #get out the tools.
    reader = ROOT.TMVA.Reader("!Color:!Silent") #activate reader

    #reader_array = len(variables) * [array.array('f', [0.])]
    for i in range(len(variables)): #add the variables into the var_array
        exec("reader_" + variables[i][0] + " = array.array('f', [0.])")
        reader.AddVariable(variables[i][0], eval("reader_" + variables[i][0]))

    dir_name = "dataset/weights/" #grab the weights and prepare the reader on what MVA will be used.
    prefixa = "Train"
    for method in methods:
        methodName = method + " method"
        weightfile = dir_name + prefixa + "_" + method + ".weights.xml"
        reader.BookMVA(methodName, weightfile)

    input_file = ROOT.TFile(test_file) #get testing data
    Tree = input_file.Get("output")

    #tree_array = len(variables) * [array.array('d', [0.])]
    for i in range(len(variables)): #set branch addresses for them to correspond to the
        exec("var_" + variables[i][0] + " = array.array('d', [0.])")
        Tree.SetBranchAddress(variables[i][0], eval("var_" + variables[i][0]))

    for method in methods:
        exec(method + "_weight = array.array('d', [0.])") #make an empty weight
        Tree.Branch(method + "_weight", eval(method + "_weight"), method + "_weight/D")

    prefix = test_file[:int(test_file.find("."))] #make the histogram and output file for the new model, now with the score.
    outputhistName = "hist_" + test_file
    outputFile = ROOT.TFile(prefix + variant + "w.root", "recreate")
    outputFile.cd()
    outputTree = Tree.CloneTree(0)

    for method in methods: #establish histograms of the distributions of scores.
        exec(method + "_score = array.array('f', [0.])")
        outputTree.Branch(method + '_score', eval(method + '_score'), method + "_score/F")
        exec("h_" + method + " = ROOT.TH1F('h_" + method + "', 'h_" + method + "', 2000,-1,1)")

    for i in range(Tree.GetEntries()):
        if i%5000 == 0:
            print("--- ... Processing event: " + str(i))
        Tree.GetEntry(i)
        for k in range(len(variables)):
            exec("reader_" + variables[k][0] + " = var_" + variables[k][0]) #load the reader array with entries of the Tree.
        for method in methods:
            exec(method + "_score[0] = reader.EvaluateMVA('"+ method + " method')") #BDT = reader.EvaluateMVA('BDT')
            #print("SCORE: " + str(eval(method + "_score[0]")))
            exec("h_" + method + ".Fill(" + method + "_score[0], " + method + "_weight[0])") #h_BDT.Fill(BDT, BDT_weight)
        outputTree.Fill()
    #print(h_BDTG3)
    exec("h_" + method + ".SetDirectory(0)")
    exec("h_" + method + ".Write()")
    outputTree.Write()
    outputFile.Close()
    print("Score assignment complete")

    #PROBLEM
    histogram_file = ROOT.TFile(outputhistName, "recreate")
    histogram_file.cd()
    for method in methods:
        exec("h_" + method + ".Write()")
    histogram_file.Close()

    return
