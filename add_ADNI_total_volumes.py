import pandas as pd
import numpy as np
import re

df = pd.read_csv("/nfs2/kimm58/ADNI_TICV_volumes.csv")

#get the BIDS tags from the filenames
#get the total brain volumes (all labels except TICV and posterior fossa)
#get the total TICV volume (all labels)

#first, get the total brain volume (all comlumns except TICV and posterior fossa and filename)
df['Total_Brain_Volume'] = df.drop(columns=['file', 'TICV', 'PosteriorFossa']).sum(axis=1, skipna=True) 
#next get the total TICV volume (total brain volume + posterior fossa + TICV)
df['Total_TICV'] = df[['Total_Brain_Volume', 'TICV', 'PosteriorFossa']].sum(axis=1, skipna=True)

#get the BIDS tags
df['sub'] = df['file'].apply(lambda x: x.split('_')[0])
df['ses'] = df['file'].apply(lambda x: x.split('_')[1])
df['acq'] = df['file'].apply(lambda x: re.search(r'acq-[A-Za-z0-9]+', x).group(0) if re.search(r'acq-[A-Za-z0-9]+', x) else '')
df['run'] = df['file'].apply(lambda x: re.search(r'run-[0-9]+', x).group(0) if re.search(r'run-[0-9]+', x) else '')

#save the dataframe
df.to_csv('/nfs2/kimm58/ADNI_TICV_volumes_BIDS.csv', index=False)