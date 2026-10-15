from lib import *
F, names = gbe.features(D, "none")
# sanity: reproduce report numbers with gbe's own design on the test split
import time
t=time.time()
# Rutledge
pR, wR, trR, teR = evaluate(F, lambda p: p[0] ** np.arange(L), [0.68], ([0.0], [0.999]))
print("Rutledge", pR, wR, "train", trR, "test", teR, time.time()-t)
pJ, wJ, trJ, teJ = evaluate(F, lambda p: jump_k(*p), [0.88, 0.42], ([0, 0], [0.999, 2]))
print("jump (gamma,kappa)", pJ, wJ, "train", trJ, "test", teJ, "vs R", 100*(teJ/teR-1))
# direct parametrization: k = (1, m' mu', m' mu'^2, ...)
direct = lambda p: np.r_[1.0, p[0] * p[1] ** np.arange(1, L)]
pD, wD, trD, teD = evaluate(F, direct, [0.5, 0.85], ([0, 0], [5, 0.999]))
print("direct (m',mu')", pD, wD, "train", trD, "test", teD, "vs R", 100*(teD/teR-1))
print("direct->jump: gamma=mu'", pD[1], "kappa=m'mu'", pD[0]*pD[1])
g,k = pJ
print("recursive: mu", g-k, "m", k/(g-k), "; direct: mu'", g, "m'", k/g)
print("B echo share", k/(1-g+k), "direct memory mass m'mu'/(1-mu')", k/(1-g), "recursive memory mass m mu/(1-mu)", (k/(g-k))*(g-k)/(1-(g-k)))
# plain check that gbe.design matches
X1 = gbe.design(F, g, k)[:, ROWS]; X2 = Xr(F, jump_k(g, k))
print("max diff vs gbe.design", np.abs(X1 - X2).max())
