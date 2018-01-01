# DL for studies for pixel vs wire readout

This runs in a Docker container at PNNL. We use python2.7 and then pip install.
I think I would advocate just using a virtual environment in python, no docker.
Download this repo, which you've already done to be seeing this, and do the following.

pip install -r requirements.txt


************************************************************************************************************************

What needs doing now for pixel/readout studies to read up Eric's Dune-like 4 APA gamma/e-/pi0 events is the follwoing.
Eric should probably do all this before collaborators can expect to do useful CNN building.

(1) Data converted from ROOT Trees in which they currently sit to numpy arrays, say.
    (a) This should work, as the trees consist of simple data types, and vectors thereof.
    (b) root2numpy should be installed, which has been a pain in the arse in the past. Eric will do this.
    OR
(2)  http://www.rootpy.org/reference/root2hdf5.html to go straight to hdf5
     (a) Currently, data is expected to be in hdf5 format before being stuffed into numpy arrays, so this may be easier.
(1) A new generator in the generator directory to read the data needs to be written
    (a) to insert labels
    (b) to insert data