from dlpix_wire.generators.base import BaseDataGenerator
import h5py
import logging
import numpy as np
import pdb
    
class Gen3D_pix(BaseDataGenerator):
  """
    Creates a generator for a list of files
  """
  logger = logging.getLogger("pixgen.gen.gen3d_pix")

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
#    self.truth = ["eminus", "eplus", "proton", "pizero", "piplus", "piminus", "muminus",  "muplus",  "kplus", "gamma"]
    self._plot=0
    self.truth = ["e-", "pi0", "gamma","p","mu"]

    self.labelvec = np.zeros(5)
    
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

    y = np.zeros((len(self.current_file['sdEvt']),250,600,250))
    ind = self.current_index
    
    self.logger.info("Binning data for event {}".format(ind))
    ### Should porbably do something here to mask out data that gets negative x's or lands in a non-central TPC. EC, 7-Jan-2018.

    data = np.array((self.current_file[ind,]['sdX'][self.current_file[ind,]['sdTPC']==3],self.current_file[ind,]['sdY'][self.current_file[ind,]['sdTPC']==3],self.current_file[ind,]['sdZ'][self.current_file[ind,]['sdTPC']==3] ))
    dataT = data.T

    if dataT.sum() is 0:
      print("Problem! Image is empty for ind " + str(ind))
      raise
    
    # dataT.shape => 3678, 3 e.g. meaning 3678 deositions.
    # Bail now if there aren't enough pixels with hits in them
    if len(self.current_file[ind,]['sdElec'][self.current_file[ind,]['sdTPC']==3]) < 500:
      self.logger.info("Bailing on this event with only {} energy depositions".format(len(self.current_file[ind,]['sdElec'][self.current_file[ind,]['sdTPC']==3])))
      status = 1
      return status

    xmin = np.argmin(dataT[:,0][dataT[:,0]>2])
    ymin = np.argmin(dataT[:,1][dataT[:,1]>2])
    zmin = np.argmin(dataT[:,2][dataT[:,2]>2])
    weights=self.current_file[ind,]['sdElec'][self.current_file[ind,]['sdTPC']==3]
                                    ##  view,chan,x
    H,edges = np.histogramdd(dataT,bins=(250,600,250),range=((0.,250.),(0.,600.),(0.,250.)),weights=weights)
#                    (Pdb) H.shape

    # Crop this back to central 2mx2mx2m about max activity point
    y = np.zeros((len(self.current_file['sdEvt']),200,200,200))
    (xmax,ymax,zmax) = np.unravel_index(np.argmax(H,axis=None),H.shape)
    # keep min past the minimal barrier, but not too close to far wall in each dimension.

    ix = np.maximum(xmax-100,0); ix = np.minimum(ix,250-200)
    iy = np.maximum(ymax-100,0); iy = np.minimum(iy,600-200)
    iz = np.maximum(zmax-100,0); iz = np.minimum(iz,250-200)

    y[ind,] = H[ix:ix+200,iy:iy+200,iz:iz+200]


    if self._plot<9:
      '''
      import matplotlib
      from mpl_toolkits.mplot3d import Axes3D
      matplotlib.use('Agg')
      import matplotlib.pyplot as plt

      fig = plt.figure()
      ax = fig.add_subplot(111, projection='3d')
      plt.imshow(y[ind,][2,])
      plt.colorbar()

      plt.savefig('scat_xy_'+str(ind)+'.png')
      ax.scatter(y[ind,])
      self._plot+=1      
      plt.close()
      '''
    

      import matplotlib
      matplotlib.use('Agg')
      import matplotlib.pyplot as plt
      from mpl_toolkits.mplot3d import Axes3D
      fig = plt.figure(1)
      fig.clf()
      ax = Axes3D(fig)
      ax.scatter(dataT[:,0],dataT[:,1],dataT[:,0],c='b',marker='o', s=3) # s=np.log10(weights/np.mean(weights))+3 )
      ax.plot([], [], c='b', marker='o')
      ax.set_xlabel('X (drift)')
      ax.set_ylabel('Y (up))')
      ax.set_zlabel('Z (beam)')
      plt.draw()
      plt.savefig('scat_xyz_'+str(ind)+'.png')
      self._plot+=1      
      plt.close()

    
    d = {}

    ptype = self._files[index].split("/")[-1].split("_")[-1].split(".")[0]
    # ptype = str(self._files[index].split("/")[-1].split("_")[0]) # "kplus", say
#    self._dataset = list(self.current_file.keys())[0]
#    self._labelset = list(self.current_file.keys())[1]

    # Setting these *set values were for hdf5 only to keep code from breaking ... I don't think these will be used elsewhere (EC, 7-Jan-2018)
    self._dataset = "image/pixels"
    self._labelset = "label/type"
    d[self._dataset] = y
    labelvectmp = np.array(self.labelvec)
#    print ("handle1evtfiles: particle and index are: " + str(ptype) + "  " + str(self.truth.index(ptype)))

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
  import signal
#  signal.signal(signal.SIGINT, debug_signal_handler)

  def next(self):
    """
      This should iterate over both files and datasets within a file.
    """


    import pdb

    multifile = False

## This line and x=np.ndarray(1,1,tmp_x...) below need to be uncommented for 3D models, not so for 2D.


    xapp = np.empty(np.append(0,np.append(1,self.current_file[self._dataset].shape[1:])))
#    xapp = np.empty(np.append(1,self.current_file[self._dataset].shape[1:]))
    yapp = np.empty(np.append(0,self.current_file[self._labelset].shape[1:]))
    nevts = 0


    while self.batch_size > nevts:
      self.file_index = int(np.random.randint(len(self._files), size=1))
#      self.current_file = h5py.File(self._files[self.file_index], 'r')
      self.current_file = np.load(self._files[self.file_index])
      self.current_index = int(np.random.randint(self.current_file.shape[0], size=1))
      if self.handlelabels(self.file_index):  # This returns non-zero if any total image electron deposition is too low
        continue
      self.filterZeros()


      self.logger.info("Reading npy file: {}".format(self._files[self.file_index]))
      multifile = True

      # self.current_file not in fact a file at this point! handlelabels() turned it into an array.
      tmp_x =  self.current_file[self._dataset][self.current_index] 


#      x = np.ndarray(shape=(1, tmp_x.shape[0],  tmp_x.shape[1],  tmp_x.shape[2]))
      x = np.ndarray(shape=(1, 1, tmp_x.shape[0],  tmp_x.shape[1],  tmp_x.shape[2]))
      x[0] = tmp_x 
      y = self.current_file[self._labelset]
      
      
      if len(x) == 0 or len(y)==0 or not len(x) == len(y):
        return next(self)

      
      xapp = np.append(xapp,x,axis=0)
      yapp = np.append(yapp,y,axis=0)

      nevts += xapp.shape[1]


    if multifile:
      return (xapp,yapp)

    tmp_x = self.current_file[self._dataset][self.current_index:self.current_index+self.batch_size]
    x = np.ndarray(shape=(1, tmp_x.shape[0],  tmp_x.shape[1],  tmp_x.shape[2]))
    x[0] = tmp_x
    y = self.current_file[self._labelset]

    if len(x) == 0 or len(y)==0 or not len(x) == len(y):
      return next(self)
    return (x,y)
