from ROOT import TFile
from root_numpy import root2array, tree2array
import numpy as np


rfile = TFile('/Users/chur558/dune-lbne/data/e-/singlepix_ana.root')
intree = rfile.Get('largana/SDTTree')
intree2 = rfile.Get('largana/MCTTree')
array = tree2array(intree)    # takes 10s of seconds.
array2 = tree2array(intree2,branches=['MCEvt','MCRun','MCSub','MCPdg','MCOrigin','MCMomentum'],selection='MCParentID==0')

##### This involves pcl'ing, and doesn't work for python3 saving and python2.7 loading or vice-versa, just FYI.
# Below saves out the G4step electron channel-deposition info
np.save("/Users/chur558/dune-lbne/data/e-/singlepix_ana_e-",array[1:10,])
# Below saves out the MCTruth info 
np.save("/Users/chur558/dune-lbne/data/e-/singlepix_truth_e-",array2[1:10,])
