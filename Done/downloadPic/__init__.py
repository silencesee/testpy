# encoding: UTF-8
from __future__ import division  #  正常除法，此导入必须置顶优先，否则报错

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import scipy.stats as stats
import scipy.optimize as opt

reload(sys)
sys.setdefaultencoding('utf-8')  #  设置变量默认编码