"""
Once a model is learned, use this to play it.
"""

from flat_game import carmunk
import numpy as np
from nn import neural_net

NUM_SENSORS = 8
GAMMA = 0.9


def play(model, weights):

    car_distance = 0
    game_state = carmunk.GameState(weights)

    # Do nothing to get initial.
    _, state, __ = game_state.frame_step((2))

    featureExpectations = np.zeros(len(weights))

    # Move.
    while True:
        car_distance += 1

        # Choose action.
        action = (np.argmax(model.predict(state, batch_size=1)))
        #print ("Action ", action)

        # Take action.
        immediateReward , state, readings = game_state.frame_step(action)
        #print ("immeditate reward:: ", immediateReward)
        #print ("readings :: ", readings)
        if car_distance > 100:
            featureExpectations += (GAMMA**(car_distance-101))*np.array(readings)
        #print ("Feature Expectations :: ", featureExpectations)
        # Tell us something.
        if car_distance % 2000 == 0:
            print("Current distance: %d frames." % car_distance)
            break


    return featureExpectations

if __name__ == "__main__":
    #saved_model = 'saved-models/goingAntiClock.h5' # [ 3529.18879523  2871.01418633   712.60264099]
    #saved_model = 'saved-models/goingClock50000.h5' #[ 1414.96678918  2883.17033785  3215.71237317]
    #saved_model = 'saved-models/clock/164-150-100-50000-25000.h5' # [ 756.72859592  723.5764696   619.23933676  0.]
    #saved_model = 'saved-models/antiClock/164-150-100-50000-25000.h5' #[ 662.72064093  689.52239795  894.57495776    0.        ]
    #saved_model = 'saved-models/antiClock/164-150-100-50000-50000.h5' #[ 676.41503823  752.38417361  753.90576239    0.        ]
    saved_model = 'saved-models_yellow/test/164-150-100-50000-25000.h5'
    #weights = [-0.41517549 ,-0.20823906  ,0.28402821 , 0.23587648  ,0.12459162 , 0.45047069 ] # around the brown obs 75000
    weights = [-0.79380502 , 0.00704546 , 0.50866139 , 0.29466834, -0.07636144 , 0.09153848 ,-0.02632325 ,-0.09672041]


    model = neural_net(NUM_SENSORS, [164, 150], saved_model)
    print (play(model, weights))
