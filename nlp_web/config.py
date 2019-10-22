import os
import synonyms

base_path = os.path.dirname(os.path.abspath(__file__))
personal_dict_path = base_path + '/data/personalDict.txt'
level_one_dict_path = base_path + '/data/level_one_dict.txt'
atmosphere_cut_path = base_path + '/data/atmosphere_cut_dict.txt'
atmosphere_filter_path = base_path + '/data/atmosphere_filter_dict.txt'
phone_path = base_path + '/data/phoneDict.txt'
music_path = base_path + '/data/custom.txt'

version = synonyms.__version__
