# DL for studies for pixel vs wire readout

This runs in a Docker container at PNNL. We use python2.7 and then pip install.
I think I would advocate just using a virtual environment in python, no docker.
Download this repo, which you've already done to be seeing this, and do the following.

pip install -r requirements.txt


************************************************************************************************************************

What needs doing now for pixel/readout studies to read up Eric's Dune-like 4 APA gamma/e-/pi0 events is the following.
Eric should probably do all this before collaborators can expect to do useful CNN building. (1) has been done enough to
allow proceeding to (2), and then eventually circling back to robustify (1).

(1) Data converted from ROOT TTrees, in which 100 evts of each type were created, to numpy arrays. (Enough to barely start to train networks,  ...)
    (a) Done by hand, thus far. I put 1 10-evt file of pi0s and e-s, each ~0.1 TB! into the data/ directory of this repo. Which is a dicey decision.
    (b) Alternatively, root2numpy which I used  by-hand so far, could be installed. One can not just pip install it (at least on OSX).
    	(i) requires root and numpy installed, then a trick. The second is easy, the first is the usual ordeal, but not hard. Cue the Hitler/Tevatron video.
	    See https://github.com/scikit-hep/root_numpy/issues/157, for the third: hints on proceeding on OSX. 
	(iii) since I don't want to include all this in the requirements of this code, for now I have converted portions of the needed TTrees on my
	      laptop where I have successfully conducted the install gymnastics. Eventually, I'll put the whole root/root_numpy into this repo.
(2) A new generator needs to be written in the generator directory to read the numpy data. (Code currently expects hdf5, which I must change.)
    (a) to insert labels to pass to models
    (b) to insert data to pass to models