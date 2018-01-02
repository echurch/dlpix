from root_numpy import root2array, tree2array

rfile = ROOT.TFile('/Users/chur558/dune-lbne/data/e-/singlepix_ana.root')
intree = rfile.Get('largana/SDTTree')
intree2 = rfile.Get('largana/MCTTree')


# Below saves out the G4step electron channel-deposition info
np.save("/Users/chur558/dune-lbne/data/e-/singlepix_ana_e-",array[1:10,])
# Below saves out the MCTruth info 
np.save("/Users/chur558/dune-lbne/data/e-/singlepix_truth_e-",array[1:10,])
