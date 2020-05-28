import numpy as np
from policy import Policy

import tensorflow.compat.v1 as tf
tf.disable_eager_execution()

class FinalModel:
    def __init__(self, env):
        # Load your Model here


        self.action_size = env.action_space.shape[0]
        self.policy = Policy(env.observation_space.shape[0] + 1, self.action_size, 0.003, 10, -1.0, None)
        self.saver = tf.train.import_meta_graph('weights/server-trained/100000_episodes.meta')
        self.saver.restore(self.policy.sess, tf.train.latest_checkpoint('weights/server-trained/'))

    def get_action(self, state):

        # scale, offset = Scaler.get()
        # scale[-1] = 1.0
        # offset[-1] = 0.0
        # change to your model
        obs = state.astype(np.float32).reshape((1, -1))
        obs = np.append(obs, [[0]], axis=1)  # add time step feature

        action = self.policy.sample(obs).reshape((1, -1)).astype(np.float32)
        return np.squeeze(action, axis=0)
