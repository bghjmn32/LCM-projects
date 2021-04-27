import os
import glob
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

folder = r'C:\LCM\Projects\KEEH\RISE\WP1_Components\SyMSpaceProjects\MopFiles'

use_all_files = False # choose to select all or just the sample files


if use_all_files:
    json_files = glob.glob(os.path.join(folder, '*.json'))
else:
    json_files = ['MopFile_3.json', 'MopFile_5.json', 'MopFile_6.json', 'MopFile_7.json']


d_labels = dict()
all_webpaths = []

for file in json_files:
    json_file = os.path.join(folder, file)
    key = os.path.basename(file)

    with open(json_file, 'r') as fh:
        content = json.load(fh)
        actual_webpaths = []
        for wp in content['webpaths']:
            '''remove strange entries'''
            for root in ['Electronics', 'KnowledgeEngines', 'Manufacturing', 'Material', 'Part', 'Simulation']:
                if wp.startswith(root):
                    actual_webpaths.append(wp)
                    break
        d_labels[key] = actual_webpaths
        all_webpaths.extend(actual_webpaths)

unique_wps = sorted(set(all_webpaths))

wp_map = dict()
for i, main_wp in enumerate(unique_wps):
    wp_map[main_wp] = i

data_labels = dict()

for main_wp in unique_wps:
    data_labels[main_wp] = []
    for file_key, webpaths in d_labels.items():
        if main_wp in webpaths:
            webpaths = list(set(webpaths))
            # webpaths.remove(main_wp)
            data_labels[main_wp].extend(webpaths)
    data_labels[main_wp] = sorted(set(data_labels[main_wp]))

data_numbers = dict()
for main_wp in unique_wps:
    data_numbers[main_wp] = [wp_map[wp] for wp in data_labels[main_wp]]

data = data_numbers
df = pd.DataFrame.from_dict(data, orient='index')
df = df.transpose()

# taking all rows but only some columns
# df = df.iloc[:,:30]

correlation_mat = df.corr()

'''plot the correlation matrix'''
if use_all_files:
    '''plot without labels'''
    sns.heatmap(correlation_mat, annot=False, xticklabels=False, yticklabels=False)
else:
    '''normal plot'''
    sns.heatmap(correlation_mat, annot=True)

plt.show()
