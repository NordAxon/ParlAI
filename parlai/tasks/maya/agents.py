from pathlib import Path
from parlai.core.teachers import ParlAIDialogTeacher
import copy
import os
""" Externally collected dataset through EmelyDataGathering. points to parlai/data/maya/ """""

def _path(opt, filtered):
    dt = opt['datatype'].split(':')[0]
    return os.path.join(opt['datapath'], 'maya', dt + '.txt')

class DefaultTeacher(ParlAIDialogTeacher):
    def __init__(self, opt, shared=None):
        opt = copy.deepcopy(opt)

        # get datafile
        opt['parlaidialogteacher_datafile'] = _path(opt, '')

        super().__init__(opt, shared)