# DL for studies for pixel vs wire readout

This runs in a Docker container at PNNL. We use python2.7 and then pip install.
I think I would advocate just using a virtual environment in python, no docker.
Download this repo, which you've already done to be seeing this, and do the following.

* pip install -r requirements.txt
* python setup.py clean
* python setup.py build
* python setup.py install
* cd dlpix_wire

example command. Note the command-line-interface usage prescribed in cli.py, in which train_nbn is one command line "hook."
* train_nbn --steps=1 --epochs=2 --history=wire-pix.json --output=wire-pix.h5 /microboone/ec/dune-root/pi0/*.npy

************************************************************************************************************************

What needs doing now for pixel/readout studies to read up Eric's Dune-like 4 APA gamma/e-/pi0 events is the following.

* A new generator needs to be written in the generator directory to read the numpy data. (Code currently expects hdf5, which I must change.)
    * to insert labels to pass to models
    * to insert data to pass to models

************************************************************************************************************************

Notes on data preparation.

* Data is converted from ROOT TTrees, in which 100 evts of each type were created, to numpy arrays.
    * Doing this by hand on my laptop where root2numpy is installed, thus far. I put one 10-evt (not even 100 evts) file of pi0s and e-s, each ~0.1 GB, into the data/ directory of this repo. 
    * Alternatively, root2numpy  could be installed in this repo. One can not just pip install it (at least on OSX).
    	* root2numpy requires root and numpy installed, then a trick for OSX to get root2numpy installed. For the trick, see https://github.com/scikit-hep/root_numpy/issues/157 for  proceeding on OSX. 
	* My by-hand procedure introduces another problem of data saving in py3 (which I have on my laptop) vs py2 (used by code in this repo), whose details you can learn in the convert_example.py here.
	* Eventually, perhaps I'll put the whole root_numpy requirements into this repo, leaving it to the user to install ROOT beforehand. (Cue the Hitler Tevatron youtube video.) But part of the goal of this Deep Learning exercise is to keep the data prep out of this repository, so let's discuss how to proceed. Perhaps data prep is a good, largely orthogonal student project.

	    
