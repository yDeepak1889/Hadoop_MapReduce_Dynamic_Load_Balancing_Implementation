from mainAlgorithm import *
from resourceReportClient import *


resources = {}
resources = getResourceStatusOfDataNodes()
implement = mainAlgorithm(resources)
implement.parametersCalc()
implement.otherParams(1, 0.8)
print(implement.R_hit)
