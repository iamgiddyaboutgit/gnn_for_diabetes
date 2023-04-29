import torch
from torch_geometric.data import Dataset, download_url
import os
import pandas as pd
from pandas import isna
from sklearn.preprocessing import LabelEncoder
import numpy as np

class DiabetesDataset(Dataset):
    def __init__(self, transform=None, pre_transform=None, datapath=None):
        super().__init__(None, transform, pre_transform)
        self.datapath = datapath

    @property
    def raw_file_names(self):
        return ['some_file_1', 'some_file_2', ...]

    @property
    def processed_file_names(self):
        return ['data_1.pt', 'data_2.pt', ...]
        

    def len(self):
        return len(self.processed_file_names)

    def get(self, idx):
        data = torch.load(osp.join(self.processed_dir, f'data_{idx}.pt'))
        return data
    
    def __parsedata():

        ref_set_le = LabelEncoder()
        ref_set_le.fit(['A', 'G', 'C', 'T', 'None'])

        data = []
        for file in os.listdir(self.datapath):
            df = pd.read_table(os.path.join(self.datapath, file))
            idx = -1
            num_padded_entries = df['node_id'].value_counts().max()
            num_sofar = 0
            processing_list = []
            for id, pos, qual, dp, end, frac, mq, mqrs, r2, rprs in  zip(df['node_id'],
                        df['POS'],
                        # df['REF'],
                        df['QUAL'],
                        df['DP'],
                        df['END'],
                        df['FractionInformativeReads'],
                        df['MQ'],
                        df['MQRankSum'],
                        df['R2_5P_bias'],
                        df['ReadPosRankSum']):
                if idx != -1 and id > idx:
                    if num_sofar < num_padded_entries:
                        to_pad = num_padded_entries - num_sofar
                        tiler = np.array([0, 0, 0, 0, 0, 0, 0, -1, 0])
                        tiled = np.tile(tiler, (to_pad, 1))
                        processing_list = np.concatenate([np.array(processing_list), tiled], axis=0)
                    
                    print(np.array(processing_list).shape)
                    data.append(processing_list)
                    processing_list = []
                    idx = id
                    num_sofar = 0
                elif idx == -1:
                    idx = id
                
                if isna(pos):
                    pos = 0

                # if isna(ref):
                #     ref = 'None'
                # ref = ref_set_le.transform([ref])[0]

                if isna(qual):
                    qual = 0

                if isna(dp):
                    dp = 0
                
                if isna(end):
                    end = 0

                if isna(frac):
                    frac = 0

                if isna(mq):
                    mq = 0

                if isna(mqrs):
                    mqrs = 0

                if isna(r2):
                    r2 = -1

                if isna(rprs):
                    rprs = 0

                processing_list.append([pos, qual, dp, end, frac, mq, mqrs, r2, rprs])
                num_sofar += 1
        data = np.array(data)