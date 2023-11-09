import illustris_python as il
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import SymLogNorm
import h5py
from tqdm import tqdm


class getBrithIDs():

    def __init__(self, basePath, snap, halo_ID):
        self.basePath = basePath
        self.snap     = snap
        self.halo_ID  = halo_ID

    def forward(self):
        fields = ['Coordinates','ParticleIDs']
        stars  = il.snapshot.loadSubhalo(self.basePath,self.snap, self.halo_ID, 'stars', fields=fields)
        tree   = il.sublink.loadTree(self.basePath, self.snap, self.halo_ID, fields=['SubfindID','SnapNum'])

        starsID = stars['ParticleIDs']

        numsnap = np.arange(0,99 + 1,1)

        progenitorID = np.zeros(stars['count']) - 1

        subhalosID = tree['SubfindID']
        subhalosSnap  = tree['SnapNum'] 
        # # Iterate on the snapshots
        for s in tqdm(numsnap, leave=True):

            # Iterate on the subhalos in that snapshot ONLY
            idx_subhalos  = np.where(subhalosSnap == s)[0]
            keep_subhalos = subhalosID[idx_subhalos]

            for i in keep_subhalos:

                # Load ID of stars in the subhalo
                subhalos_starsID = il.snapshot.loadSubhalo(self.basePath,s, i, 'stars', fields=['ParticleIDs'])

                not_already_IDed = np.where(progenitorID == -1)[0]
                stars_in = np.isin(starsID[not_already_IDed], subhalos_starsID)

                indices = not_already_IDed[stars_in]
                progenitorID[indices] = i

        return stars['Coordinates'], progenitorID

    