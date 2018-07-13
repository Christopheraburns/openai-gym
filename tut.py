import gym
import gym.spaces
import gym.utils

G = 0 # cumulative Reward
statehistory = []
rewardhistory = [] # assumes a start of Zero
timesteps = 0 # total number of steps within the current episode
env = gym.make("Taxi-v2")
startstate = env.reset()


def launchrandom():
    timesteps = 0
    reward = None
    statehistory.append(startstate)
    rewardhistory.append(0)
    while reward != 20:
        state, reward, done, info = env.step(env.action_space.sample())
        timesteps += 1
        statehistory.append(state)
        rewardhistory.append(reward)
    return timesteps



def printrules():
    global env
    taxi = " "
    taxi = gym.utils.colorize(taxi, "yellow", highlight=True)
    pickup = "Blue"
    pickup = gym.utils.colorize(pickup, "blue", highlight = True)
    dropoff = "Purple"
    dropoff = gym.utils.colorize(dropoff,"magenta", highlight = True)
    print("The yellow square {} represents the Taxi".format(taxi))
    print("There are FOUR locations within the environment - represented by Letters (Y,G,B,R)")
    print("The locations are in fixed locations but they are randomly placed in those locations")
    print("The {} letter represents the PICKUP location".format(pickup))
    print("The  {} letter represents the DROP-OFF location".format(dropoff))
    print("The '|' represents a wall")
    print("You receive +20 [reward] points for a successful dropoff")
    print("You lose 1 [reward] point for every timestep it takes")
    print("There is also a 10 point penalty for illegal pick-up and drop-off actions. This includes hitting a wall")
    env.render()



def getInput():
    global timesteps
    if timesteps < 1:
        direction = input("Use the N,S,E,W,P,D keys to move the taxi:")
    else:
        direction = input("Continue to move the taxi with the N,S,E,W,P,D  keys:")
    timesteps += 1
    loop(direction)

def loop(direction):
    complete = False
    global timesteps
    global env
    global startstate
    global G
    global statehistory
    global rewardhistory
    if timesteps == 0:
        statehistory.append(startstate)
        rewardhistory.append(0)
        print()
        print("Starting new Episode...")
        print()
        print('possible environment states: {}.  Current State = {}'.format(env.observation_space, startstate))
        print('possible actions: {} - North East South West Pickup DropOff'.format(env.action_space.n))
        print('use the keys N, E, S, W, P, D for the above actions')
        print('enter the H key for help')
        print('enter the R key to launch a random AI taxi')
        # North = Up = 1, East = Right = 2, South = Down = 0, West = Left = 3, Pickup = 4, DropOff = 5
        print('Current reward = {}'.format(G))
        env.render()
    if direction is not None:
        switch = {
            "s": 0,
            "n": 1,
            "e": 2,
            "w": 3,
            "p": 4,
            "d": 5,
            "h": 6,
            "r": 7
        }

        step = switch.get(direction.lower(), "Invalid")

        if step is not "Invalid":
            if step is not 6:
                if step == 5:
                    print("Dropping off!")
                elif step == 4:
                    print("Picking up!")
                elif step == 7:
                    # Launch and AI randomized Taxi
                    timesteps -= 1  # don't count this as a move
                    aisteps = launchrandom()
                    print("AI taxi took {} steps to complete the episode".format(aisteps))
                    complete = True
                    print(rewardhistory)

                    getInput()
                else:
                    print('Moving the Taxi {}'.format(direction))
                state, reward, done, info =  env.step(step)
                G += reward
                statehistory.append(state)
                rewardhistory.append(reward)
                print("Action reward = {}".format(reward))
                print("Episode cumulative reward = {}".format(G))
                print("New state = {}".format(state))
                print("Timesteps = {}".format(timesteps))
                if done:
                    complete = True

                env.render()
            else:
                timesteps -= 1 # don't count this as a move
                printrules()

    if not complete:
        getInput()
    else:
        print("The episode is complete!")
        # TODO - Print final state, reward, etc.




loop(None)
