#!/usr/bin/env python

import numpy as np

from pycrazyswarm import *
import yaml

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    with open("../launch/heights.yaml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)


    # fig8_traj = piecewise.loadcsv('traj/trajectory.csv')
    # fig8_traj = piecewise.loadcsv('traj/output.csv')

    trajs = []
    for i in range(len(allcfs.crazyflies)):
        trajs.append(piecewise.loadcsv('traj/trajectory' + str(i) + '.csv'))

    TRIALS = 1
    for i in range(TRIALS):
        for index, cf in enumerate(allcfs.crazyflies):
            cf.uploadTrajectory(trajs[index])

        for cf in allcfs.crazyflies:
            cf.takeoff(targetHeight=cfg[cf.id], duration=2.0)
        # allcfs.takeoff(targetHeight=1.0, duration=2.0)
        timeHelper.sleep(2.5)

        for cf in allcfs.crazyflies:
            pos = np.array(cf.initialPosition) + np.array([0, 0, float(cfg[cf.id])])
            cf.hover(pos, 0, 2.0)
        timeHelper.sleep(2.5)

        t = max(cfsim.cffirmware.piecewise_duration(traj) for traj in trajs)
        print "times", [cfsim.cffirmware.piecewise_duration(traj) for traj in trajs]
        for cf in allcfs.crazyflies:
            cf.light_switch(True)

        allcfs.startTrajectory()
        timeHelper.sleep(t)

        for cf in allcfs.crazyflies:
            cf.light_switch(False)

        # allcfs.startTrajectoryReversed()
        # timeHelper.sleep(90.0) # TODO...

        allcfs.land(targetHeight=0.06, duration=2.0)
        timeHelper.sleep(3.0)
