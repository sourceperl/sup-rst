# -*- coding: utf-8 -*-

from pySupRST.main import sup_rst
from pprint import pprint

c= sup_rst()

a = c.get_tm("RTR_P_DG1")

pprint(a)
