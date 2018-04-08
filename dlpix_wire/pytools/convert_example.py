from ROOT import TFile
from root_numpy import root2array, tree2array
import numpy as np


rfile = TFile('/Users/chur558/dune-lbne/data/e-/singlepix_ana_e-.root')
intree = rfile.Get('largana/SDTTree')
print ("e- events:"+str(intree.GetEntries()))
intree2 = rfile.Get('largana/MCTTree')
array = tree2array(intree)    # takes 10s of seconds.
array2 = tree2array(intree2,branches=['MCEvt','MCRun','MCSub','MCPdg','MCOrigin','MCMomentum'],selection='MCParentID==0')

##### This involves pcl'ing, and doesn't work for python3 saving and python2.7 loading or vice-versa, just FYI.
# Below saves out the G4step electron channel-deposition info
np.save("/Users/chur558/dune-lbne/data/e-/singlepix_ana_e-",array)
# Below saves out the MCTruth info 
np.save("/Users/chur558/dune-lbne/data/e-/singlepix_truth_e-",array2)


rfile = TFile('/Users/chur558/dune-lbne/data/mu/singlepix_ana_mu.root')
intree = rfile.Get('largana/SDTTree')
print ("mu events:"+str(intree.GetEntries()))
intree2 = rfile.Get('largana/MCTTree')
array = tree2array(intree)    # takes 10s of seconds.
array2 = tree2array(intree2,branches=['MCEvt','MCRun','MCSub','MCPdg','MCOrigin','MCMomentum'],selection='MCParentID==0')

##### This involves pcl'ing, and doesn't work for python3 saving and python2.7 loading or vice-versa, just FYI.
# Below saves out the G4step electron channel-deposition info
np.save("/Users/chur558/dune-lbne/data/mu/singlepix_ana_mu",array)
# Below saves out the MCTruth info 
np.save("/Users/chur558/dune-lbne/data/mu/singlepix_truth_mu",array2)


rfile = TFile('/Users/chur558/dune-lbne/data/pi0/singlepix_ana_pi0.root')
intree = rfile.Get('largana/SDTTree')
print ("pi0 events:"+str(intree.GetEntries()))
intree2 = rfile.Get('largana/MCTTree')
array = tree2array(intree)    # takes 10s of seconds.
array2 = tree2array(intree2,branches=['MCEvt','MCRun','MCSub','MCPdg','MCOrigin','MCMomentum'],selection='MCParentID==0')

##### This involves pcl'ing, and doesn't work for python3 saving and python2.7 loading or vice-versa, just FYI.
# Below saves out the G4step electron channel-deposition info
np.save("/Users/chur558/dune-lbne/data/pi0/singlepix_ana_pi0",array)
# Below saves out the MCTruth info 
np.save("/Users/chur558/dune-lbne/data/pi0/singlepix_truth_pi0",array2)


rfile = TFile('/Users/chur558/dune-lbne/data/p/singlepix_ana_p.root')
intree = rfile.Get('largana/SDTTree')
print ("p events:"+str(intree.GetEntries()))
intree2 = rfile.Get('largana/MCTTree')
array = tree2array(intree)    # takes 10s of seconds.
array2 = tree2array(intree2,branches=['MCEvt','MCRun','MCSub','MCPdg','MCOrigin','MCMomentum'],selection='MCParentID==0')

##### This involves pcl'ing, and doesn't work for python3 saving and python2.7 loading or vice-versa, just FYI.
# Below saves out the G4step electron channel-deposition info
np.save("/Users/chur558/dune-lbne/data/p/singlepix_ana_p",array)
# Below saves out the MCTruth info 
np.save("/Users/chur558/dune-lbne/data/p/singlepix_truth_p",array2)



rfile = TFile('/Users/chur558/dune-lbne/data/gamma/singlepix_ana_gamma.root')
intree = rfile.Get('largana/SDTTree')
print ("gamma events: "+str(intree.GetEntries()))
intree2 = rfile.Get('largana/MCTTree')
array = tree2array(intree)    # takes 10s of seconds.
array2 = tree2array(intree2,branches=['MCEvt','MCRun','MCSub','MCPdg','MCOrigin','MCMomentum'],selection='MCParentID==0')

##### This involves pcl'ing, and doesn't work for python3 saving and python2.7 loading or vice-versa, just FYI.
# Below saves out the G4step electron channel-deposition info
np.save("/Users/chur558/dune-lbne/data/gamma/singlepix_ana_gamma",array)
# Below saves out the MCTruth info 
np.save("/Users/chur558/dune-lbne/data/gamma/singlepix_truth_gamma",array2)


