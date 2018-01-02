from root_numpy import root2array, tree2array

rfile = ROOT.TFile('/Users/chur558/dune-lbne/data/e-/singlepix_ana.root')
intree = rfile.Get('largana/SDTTree')
np.save("/Users/chur558/dune-lbne/data/e-/singlepix_ana_e-",array[1:10,])
