# DL for studies for pixel vs wire readout

This runs in a Docker container at PNNL. We use python3.5 and then pip install.
I think I would advocate just using a virtual environment in python, no docker.
Download this repo, which you may've already done to be seeing this, and do the following.

* pip install -r requirements.txt
* python setup.py clean
* python setup.py build
* python setup.py install
* cd dlpix_wire

Note the command-line-interface usage prescribed in cli.py, in which train_vgg and train_nbn3D are two command line "hooks."

After editing any python, hop back up to dlpix and do 'python setup.py install'. 

************************************************************************************************************************

 pixel/readout studies are in the following state:

* A data generator exists in the generator directory to read the numpy wire-time data, converted from Eric's DUNE-like 4 APA root-file simulations.
    * The above train_vgg command will in principle run a VGG16-like network to learn on pi0s, gammas, e-s.
    * train_vgg --steps=1 --epochs=20 --history=wire-pix.json --output=wire-pix.h5 data/\*/singlepix_ana_\*.npy
* A new generator exists to parse the pixel data and run/train/infer on the pixel data too. 
    * train_nbn3D --steps=1 --epochs=10 --history=wire-pix.json  --output=wire-pix.h5 data/\*/singlepix_ana_\*.npy
    * 3D CNN in gen3D_pixel_npy.py has lots of room for improvement.
* Not obvious either of above is learning. Let's make sure labels are correct, etc.

************************************************************************************************************************

Notes on data preparation.

* Data is converted from ROOT TTrees, in which  200 evts of each type -- pi0,e-,gamma -- were created, to numpy arrays.
    * Doing this by hand on my laptop where root2numpy is installed, thus far. I put files of *only 20 evts* of pi0s, gammas and e-s, each ~25 MB, into the data/ directory of this repo.  See pytools/convert_example.py in this repo for the script I used. We will need to shuttle around bigger files with more events by some means other than github.
    * Alternatively to doing conversion by hand in a private location each time, root2numpy  could be installed in this repo. One issue is that one can not just pip install it (at least on OSX). In fact, installing many python pkgs on OSX seems troublesome.
    	* root2numpy requires root and numpy installed, then a trick for OSX to get root2numpy installed. For the trick, see https://github.com/scikit-hep/root_numpy/issues/157 for  proceeding on OSX. Also, heads-up: do not np.save() with py2/3 and try to np.load() the file back with py3/2. Consistency is demanded.
	* Eventually, perhaps I'll put the whole root_numpy requirements into this repo, leaving it to the user to install ROOT beforehand. (Cue the Hitler Tevatron youtube video.) But part of the goal of this Deep Learning exercise is to keep the data prep out of this repository, so let's discuss how to proceed. Perhaps data prep is a good, largely orthogonal student project.

	    
