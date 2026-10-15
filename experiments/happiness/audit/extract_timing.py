import os, numpy as np, scipy.io, time
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data", "gbe")
t=time.time()
S = scipy.io.loadmat(os.path.join(DATA, "extracted", "Rutledge_GBE_risk_data_TOD.mat"), struct_as_record=False, squeeze_me=True)["subjData"]
print("loaded", time.time()-t)
plays = []
for i, s in enumerate(S):
    d = s.data
    mats = [d] if isinstance(d, np.ndarray) and d.dtype != object else list(np.atleast_1d(d))
    for X in mats:
        X = np.asarray(X, dtype=float)
        if X.shape != (30, 15): continue
        plays.append(X[:, [0, 8, 10, 11, 13, 2, 9]])
P = np.stack(plays)
print(P.shape)
np.savez_compressed(os.path.join(DATA, "extra.npz"), trial=P[...,0], lat=P[...,1], start=P[...,2], rrt=P[...,3], spin=P[...,4], c=P[...,5], h=P[...,6])
