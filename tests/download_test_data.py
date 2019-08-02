"""Download test data."""
import os
import os.path as op

import datalad.api as dl

from mne.commands.utils import get_optparser


def _provide_testing_data(dataset):
    """Return dict of dataset, and the corresponding URLs."""
    urls_dict = {
        'ds000248': 'https://github.com/OpenNeuroDatasets/ds000248',
        'ds000117': 'https://github.com/OpenNeuroDatasets/ds000117',
        'ds001810': 'https://github.com/OpenNeuroDatasets/ds001810',
        'ds001971': 'https://github.com/OpenNeuroDatasets/ds001971',
    }
    if dataset is None:
        return urls_dict
    else:
        return {dataset: urls_dict[dataset]}


def _provide_get_dict(dataset):
    """Return dict of dataset, and which data to get from it."""
    get_dict = {
        'ds000248': ['sub-01'],
        'ds000117': ['sub-01/ses-meg/meg/sub-01_ses-meg_task-facerecognition_coordsystem.json',  # noqa: E501
                     'sub-01/ses-meg/meg/sub-01_ses-meg_task-facerecognition_run-01_events.tsv',  # noqa: E501
                     'sub-01/ses-meg/meg/sub-01_ses-meg_task-facerecognition_run-01_meg.fif',  # noqa: E501
                     'sub-01/ses-meg/meg/sub-01_ses-meg_headshape.pos'
                     ],
        'ds001810': ['sub-01/ses-anodalpre'],
        'ds001971': ['sub-001'],
    }
    if dataset is None:
        return get_dict
    else:
        return {dataset: get_dict[dataset]}


# Download the testing data
if __name__ == '__main__':

    parser = get_optparser(__file__, usage="usage: %prog -dataset DATASET")
    parser.add_option('-d', '--dataset', dest='dataset',
                      help='Name of the dataset', metavar='INPUT',
                      default=None)
    opt, args = parser.parse_args()
    dataset = opt.dataset if opt.dataset != '' else None

    # Save everything in ~/data
    data_dir = op.join(op.expanduser('~'), 'data')
    if not op.exists(data_dir):
        os.makedirs(data_dir)

    urls_dict = _provide_testing_data(dataset)
    get_dict = _provide_get_dict(dataset)

    for dsname, url in urls_dict.items():
        print('\n----------------------')
        dspath = op.join(data_dir, dsname)
        # install the dataset
        print('datalad installing "{}"'.format(dsname))
        dataset = dl.install(path=dspath, source=url)

        # get the first subject
        for to_get in get_dict[dsname]:
            print('datalad get data "{}" for "{}"'.format(to_get, dsname))
            dataset.get(to_get)
