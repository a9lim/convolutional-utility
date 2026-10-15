"""What an impulse test can see of adaptation: the largest negative lobe a 5-minute play can leave at the
gaps of carryover.py, over every adaptation time constant, against the data's intervals. No data needed."""
import numpy as np
# A pulse of size A lasting d minutes; EMA reference with time constant tau (minutes); felt e = u - h r.
# After the pulse the felt lobe at gap g is -h A (1 - exp(-d/tau)) exp(-g/tau). The largest lobe any tau can
# produce at gap g, as a share of the pulse (h = 1), against the data's 95% intervals:
d = 5.0
taus = np.logspace(-1, 6, 4000)
for g, ci in [(4.4, "[+40, +50]"), (21.9, "[+5, +44]"), (578.3, "[-1, +21]"), (3464.2, "[-5, +17]"), (55299.7, "[-16, +11]")]:
    lobe = (1 - np.exp(-d / taus)) * np.exp(-g / taus)
    i = lobe.argmax()
    print(f"gap {g:8.1f} min: largest possible lobe {100 * lobe[i]:6.2f}% of the pulse (at tau = {taus[i]:8.1f} min); data {ci}")
# step response: a sustained change keeps r rising, so adaptation shows in full: e(t) = A (1 - h (1 - exp(-t/tau)))
print("step: after a sustained change of size A, felt level -> A(1-h): the whole lobe accumulates")
