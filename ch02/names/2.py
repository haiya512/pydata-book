import pandas as pd
from pandas import pivot_table
import numpy as np
years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']
for year in years:
    path = "/Users/bobo/gitcenter/pydata-book/ch02/names/yob%d.txt" % year
    frame = pd.read_csv(path, names=columns)
    frame['year'] = year
    pieces.append(frame)

names = pd.concat(pieces, ignore_index=True)
# print names[:2]
total_births = pivot_table(names,
                           values='births',
                           columns='sex',
                           ndex=['year'],
                           aggfunc='sum')


def add_prop(group):
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group


names = names.groupby(['year', 'sex']).apply(add_prop)
np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)


def get_top1000(group):
    return group.sort_index(by="births", ascending=False)[:1000]


grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)
pieces = []
for year, group in names.groupby(['year', 'sex']):
    pieces.append(group.sort_index(by='births', scending=False)[:1000])
top1000 = pd.concat(pieces, ignore_index=True)

print top1000[:2]
