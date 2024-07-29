import numpy as np

cloud = np.array([374, 357, 350, 343, 356, 351])
print("Mean of AWS:", cloud.mean())
print("Std of AWS:", cloud.std())

local = np.array([22590, 22648, 23074, 23082, 23129, 24414])
local = local / 60

print("Mean of local:", local.mean())
print("Std of local:", local.std())