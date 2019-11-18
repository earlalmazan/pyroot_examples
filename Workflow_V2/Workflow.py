import ROOT
import os
import sys
import Training
import Application
import Preparation

user_input = input("Config File Name: \n")
if user_input == "":
    user_input = "config.txt"
while not os.path.exists(user_input):
    print("\nConfig File Not Found.\n")
    user_input = input("\nConfig File Name: \n")
    if user_input == "":
        user_input = "config.txt"

config_file = open(user_input, "r") #config file overview.
variables = []
methods = []
modes = [] #Pre-Selection, Training, Application
src_file = ""
variant = ""
for line in config_file:
    if line[:1] != "#":
        if line[:8] == "variable":
            variables.append(line[9:].strip().split())
        if line[:6] == "method":
            methods.append(line[7:].strip())
        if line[:4] == "mode":
            modes.append(line[5:].strip())
        if line[:8] == "src_file":
            src_file = line[9:].strip()
        if line[:8] == "test_con":
            test_con = line[9:].strip()
        if line[:9] == "train_con":
            train_con = line[10:].strip()
        if line[:7] == "sig_con":
            sig_con = line[8:].strip()
        if line[:7] == "bkg_con":
            bkg_con = line[8:].strip()
        if line[:7] == "variant":
            variant = line[8:].strip()
config_file.close()
if len(variables) == 0:
    print("No Variables Specified in Config File")
    sys.exit(1)
if len(methods) == 0:
    print("No Method Specified in Config File")
    sys.exit(1)
if len(modes) == 0:
    print("No Mode Specificied in Config File (Training, Application, Pre-Selection)")
    sys.exit(1)
if src_file == "":
    print("No Source File for Reference Found in config file")
    sys.exit(1)
if variant != "":
    variant = "_" + variant
sig_file = src_file.rpartition(".")[0] + variant + "_sig.root"
bkg_file = src_file.rpartition(".")[0] + variant + "_bkg.root"
mdl_file = src_file.rpartition(".")[0] + variant + "_TMVA.root"

#variable screening
src_file_open = ROOT.TFile.Open(src_file)
src_tree = src_file_open.Get("output")
new_variables = []
for variable in variables:
    print(variable)
    try:
        print(getattr(src_tree, variable[0]))
        new_variables.append(variable)
    except AttributeError:
        print("Variable not found in source tree")
    except:
        new_variables.append(variable)
variables = new_variables
print(new_variables)

if "Preparation" in modes:
    Preparation.cut(src_file, sig_file, bkg_file, test_con, train_con, sig_con, bkg_con)
if "Training" in modes:
    Training.train(sig_file, bkg_file, mdl_file, variables, methods, test_con, train_con)
if "View" in modes:
    Training.view(mdl_file)
if "Application" in modes:
    Application.apply(src_file, variables, methods, variant)
