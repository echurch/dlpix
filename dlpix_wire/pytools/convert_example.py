from ROOT import TFile
from root_numpy import root2array, tree2array


rfile = TFile('/Users/chur558/dune-lbne/data/e-/singlepix_ana.root')
intree = rfile.Get('largana/SDTTree')
intree2 = rfile.Get('largana/MCTTree')
array = tree2array(intree)
array2 = tree2array(intree2)

##### This involves pcl'ing, and doesn't work for python3 saving and python2.7 loading!
# Below saves out the G4step electron channel-deposition info
#np.save("/Users/chur558/dune-lbne/data/e-/singlepix_ana_e-",array[1:10,])
# Below saves out the MCTruth info 
#np.save("/Users/chur558/dune-lbne/data/e-/singlepix_truth_e-",array[1:10,])


np.savetxt("/Users/chur558/dune-lbne/data/e-/singlepix_ana_e-.gz",array[1:10,])
np.savetxt("/Users/chur558/dune-lbne/data/e-/singlepix_truth_e-.gz",array2[1:10,])
