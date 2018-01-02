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
    (b) root2numpy could be installed, which has been a pain in the arse in the past.  Can not just pip install it (at least on OSX).
    	(i) requires root and numpy installed. The second is easy, the first is the usual ordeal. Cue the Hitler/Tevatron video.
	(ii) Then see https://github.com/scikit-hep/root_numpy/issues/157, ...
	(iii) since I don't want to include all this in the requirements of this code, for now I will convert the needed TTrees on my
	      laptop where I have successfully conducted the install gymnastics, and provide the numpy .dat files  to interested parties.
(2) A new generator needs to be written in the generator directory to read the data
    (a) to insert labels
    (b) to insert data