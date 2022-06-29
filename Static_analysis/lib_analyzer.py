# lib_analyzer.py

import sys
sys.path.insert(1, 'C:\Age_Rating\LiteRadar\LiteRadar')
from literadar import LibRadarLite

def analyze_lib(apk_path):
    lrd = LibRadarLite(apk_path)
    res = lrd.compare()

    return res