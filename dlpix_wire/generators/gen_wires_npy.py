from dlpix_wire.generators.base import BaseDataGenerator
import h5py
import logging
import numpy as np
import pdb
    
class Gen_wires(BaseDataGenerator):
  """
    Creates a generator for a list of files
  """
  logger = logging.getLogger("pixgen.gen.gen_wires")

  def __init__(self, datapaths, datasetname, 
               labelsetname, batch_size=10, middle=False):
    self._files = [ i for i in datapaths]
    import random
    random.shuffle(self._files)

    self._middle = middle
    self._dataset = datasetname
    self._labelset = labelsetname
    self.batch_size = batch_size
    self.file_index=0
    self.current_index=0
    self._plot=0
#    self.truth = ["eminus", "eplus", "proton", "pizero", "piplus", "piminus", "muminus",  "muplus",  "kplus", "gamma"]

#    self.truth = ["e-", "pi0", "gamma", "p", "mu"]
    self.truth = ["pi0", "p", "mu"]

    self.labelvec = np.zeros(3)
    
    self.logger.info("Initializing npy file object with value: {}".format(self._files[self.current_index]))


    self.file_index = int(np.random.randint(len(self._files), size=1))
#    self.current_file = h5py.File(self._files[self.file_index], 'r')

    self.current_file = np.load(self._files[self.file_index])
    self.current_index = int(np.random.randint(self.current_file.shape[0], size=1))
    self.handlelabels(self.file_index)
    self.filterZeros()


  def filterZeros(self):
    # set low ADC pixels to 0
    pass

  def handlelabels(self,index):
    status = 0

#    x = self.current_file['image']['wires'] # from hdf5 days.

# Must bin the data evt-by-evt, since each event has different number of data elements (sim charge depositions)


    y = np.zeros((len(self.current_file['sdEvt']),3,600,500)) # limit ourselves to 1200 wire span
    ind = self.current_index
    
    self.logger.info("Binning data for event {}".format(ind))
    ### Should probably do something here to mask out data that gets negative x's or lands in a non-central TPC. EC, 7-Jan-2018.
    ### In fact, replace integer bin numbers below with actual bounds on bins
    
    data = np.array((self.current_file[ind,]['sdView'][self.current_file[ind,]['sdTPC']==3],self.current_file[ind,]['sdChan'][self.current_file[ind,]['sdTPC']==3],self.current_file[ind,]['sdX'][self.current_file[ind,]['sdTPC']==3] ))
    dataT = data.T
    if data.sum() is 0:
      print ("Scream/complain: Empty image. ind is " + str(ind))
      raise

    # Bail now if there aren't enough pixels with hits in them
    if len(self.current_file[ind,]['sdElec'][self.current_file[ind,]['sdTPC']==3]) < 500:
      self.logger.info("Bailing on this event with only {} energy depositions".format(len(self.current_file[ind,]['sdElec'][self.current_file[ind,]['sdTPC']==3])))
      status = 1
      return status

    # dataT.shape => 3678, 3 e.g. meaning 3678 depositions.
                                    ##  view,chan,x
    dataT2 = dataT

    minchanguess = np.array([2700.,2700.,4900]) # rough-rough guess min channel #s for planes 0,1,2, in TPC3

    # let's not use min possible channel, but min channel with activity in it:

    mask = (dataT2[:,1][dataT2[:,0]==0] > 2.0)  # 2.0 being some minimum activity
    ind0 = np.argmin(dataT2[:,1][dataT2[:,0]==0][mask])
    mask = (dataT2[:,1][dataT2[:,0]==1] > 2.0)  # 2.0 being some minimum activity
    ind1 = np.argmin(dataT2[:,1][dataT2[:,0]==1][mask])
    mask = (dataT2[:,1][dataT2[:,0]==2] > 2.0)  # 2.0 being some minimum activity
    ind2 = np.argmin(dataT2[:,1][dataT2[:,0]==2][mask])
    minpossible = np.array( [dataT2[:,1][dataT2[:,0]==0][ind0],dataT2[:,1][dataT2[:,0]==0][ind1],dataT2[:,1][dataT2[:,0]==2][ind2]] )
                                                               
    minchan = np.amax(np.row_stack((minpossible-100,minchanguess)),axis=0)  # try to show trailing 100 wires, but not if it goes below true physical min wire.
    
    dataT2[:,1][dataT2[:,0]==0] -= minchan[0]
    dataT2[:,1][dataT2[:,0]==1] -= minchan[1]
    dataT2[:,1][dataT2[:,0]==2] -= minchan[2]
    H,edges = np.histogramdd(dataT,bins=(3,600,500),range=((0.,3.0),(0.,600.),(0.,250.)),weights=self.current_file[ind,]['sdElec'][self.current_file[ind,]['sdTPC']==3])
#                    (Pdb) H.shape
#                    (3, 2560, 3200)
#                    
    y[ind,] = H

    
    if self._plot<9:
      import matplotlib
      matplotlib.use('Agg')
      import matplotlib.pyplot as plt

      plt.imshow(y[ind,][0,])
      plt.savefig('scat_U_'+str(ind)+'.png')
      plt.close()
      plt.imshow(y[ind,][2,])

      plt.savefig('scat_Z_'+str(ind)+'.png')
      self._plot+=1      
      plt.close()

        

    d = {}

    ptype = self._files[index].split("/")[-1].split("_")[-1].split(".")[0]
    # ptype = str(self._files[index].split("/")[-1].split("_")[0]) # "kplus", say
#    self._dataset = list(self.current_file.keys())[0]
#    self._labelset = list(self.current_file.keys())[1]

    self._dataset = "image/wires"
    self._labelset = "label/type"
    d[self._dataset] = y
    labelvectmp = np.array(self.labelvec)
#      print "handle1evtfiles: particle and index are: " + str(ptype) + "  " + str(self.truth.index(ptype))
    labelvectmp[self.truth.index(ptype)] = 1


    d[self._labelset] = np.expand_dims(labelvectmp,axis=0)
    self.current_file = d
    return status

  @property
  def output(self):
    current_index= self.current_index
    file_index = self.file_index

    x,y = next(self)
    self.current_index =current_index
    self.file_index = file_index
    return x[0].shape

  @property
  def input(self):
    current_index= self.current_index
    file_index = self.file_index
    x,y = next(self)
    self.current_index =current_index
    self.file_index = file_index
    return y[0].shape[0]

  def __len__(self):
    """
      Iterates over files to create the total sum length
      of the datasets in each file.
    """
    ### uggh. This is v slow, especially with tons of 1-event files.
#    return sum([h5py.File(i,'r')[self._dataset].shape[0] for i in self._files] )
    ### Let's just take a guess. Not sure we use this number anyway.
#    return len(self._files) * h5py.File(self._files[0],'r')[self._dataset].shape[0] 
    return 12

  def __next__(self):
    return self.next()
  
  def debug_signal_handler(signal, frame):
    import pdb
    pdb.set_trace()
#  import signal
#  signal.signal(signal.SIGINT, debug_signal_handler)

  def next(self):
    """
      This should iterate over both files and datasets within a file.
    """


#    import pdb

    multifile = False

## This line and xapp.append below need to be uncommented for 3D models, not so for 2D.
#    xapp = np.empty(np.append(0,np.append(1,self.current_file[self._dataset].shape[1:])))
    xapp = np.empty(np.append(0,self.current_file[self._dataset].shape[1:]))
    yapp = np.empty(np.append(0,self.current_file[self._labelset].shape[1:]))

    nevts = 0

    while self.batch_size > nevts:
      self.file_index = int(np.random.randint(len(self._files), size=1))
#      self.current_file = h5py.File(self._files[self.file_index], 'r')
      self.current_file = np.load(self._files[self.file_index])
      self.current_index = int(np.random.randint(self.current_file.shape[0], size=1))
      if self.handlelabels(self.file_index): # This returns non-zero if any total image electron deposition is too low
        continue
      
      self.filterZeros()


      self.logger.info("Reading npy file: {}".format(self._files[self.file_index]))
      multifile = True
      # self.current_file not in fact a file at this point! handlelabels() turned it into an array.
      tmp_x =  self.current_file[self._dataset][self.current_index] 


      x = np.ndarray(shape=(1, tmp_x.shape[0],  tmp_x.shape[1],  tmp_x.shape[2]))
#      x = np.ndarray(shape=(1, 1, tmp_x.shape[0],  tmp_x.shape[1],  tmp_x.shape[2]))
      x[0] = tmp_x 
      y = self.current_file[self._labelset]

      if len(x) == 0 or len(y)==0 or not len(x) == len(y):
        return next(self)

      xapp = np.append(xapp,x,axis=0)
      yapp = np.append(yapp,y,axis=0)
      nevts += 1

    if multifile:
      return (xapp,yapp)  # [:, 2:3,:,:] -- only Collection. (2:3 means 2. Whereas 2:2 will collapse the array by one dimension.)

    tmp_x = self.current_file[self._dataset][self.current_index:self.current_index+self.batch_size]
    x = np.ndarray(shape=(1, tmp_x.shape[0],  tmp_x.shape[1],  tmp_x.shape[2]))
    x[0] = tmp_x
    y = self.current_file[self._labelset]

    if len(x) == 0 or len(y)==0 or not len(x) == len(y):
      return next(self)
    return (x,y)
