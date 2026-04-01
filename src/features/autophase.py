import numpy as np

def extract_autophase(env):
    raw = env.observation["Autophase"]
    features = np.array(raw, dtype=np.float32)
    return np.log1p(features)

AUTOPHASE_DIM = 56