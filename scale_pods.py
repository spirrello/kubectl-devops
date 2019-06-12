#!/usr/bin/python
import argparse
import os
import time


"""
Quick/dirty script for scaling deployments in all or individual namespaces.

Arguments:
ns     Specify which namespace you wish to scale deployments.  If no namespace is entered,
       all namespaces will be in scopeself.  They can be comma delimited.

replicas  Number of pods to scale each deployment to.  Default is 0.

time   Amount of time to pause in between scaling executions.  Default is 10 seconds.

"""

def getNamespaces():
    """
    Function for fetching Namespaces
    """

    print("Fetching all namespaces...")

    #Get the list of NS and then clean up the list
    tempNameSpacesList = os.popen("kubectl get ns | grep -v NAME | awk '{print $1}'")
    tempNameSpacesList = tempNameSpacesList.read().split('\n')
    nameSpacesList = [x for x in tempNameSpacesList if x]

    #Remove kube-system from the list.
    #We want to scale kube-system intentionally, via --ns kube-system
    nameSpacesList.remove('kube-system')

    return nameSpacesList


def scaleJobs(ns,sleepTime=None,replicas=None):
    """
    Function for scaling deployments
    """
    #Assign a default value if necessary

    if sleepTime == None:
        sleepTime = 10

    if replicas == None:
        replicas = 0

    getDeploymentCommand = "kubectl get jobs -n " + ns + " | grep -v NAME | awk '{print $1}'"

    tempDeploymentList = os.popen(getDeploymentCommand)
    tempDeploymentList = tempDeploymentList.read().split('\n')
    deploymentList = [deploy for deploy in tempDeploymentList if deploy]

    if len(deploymentList) > 0:
        print("\nDeployments for {0} namespace:\n{1}".format(ns,deploymentList))

        for deploymentItem in deploymentList:
            scaleCommand = "kubectl scale jobs " + deploymentItem + " -n " + ns + " --replicas=" + str(replicas)
            print(scaleCommand)
            scaleResult = os.popen(scaleCommand)
            print(scaleResult.read())
            #Sleep for a period to dial down the churn.
            time.sleep(int(sleepTime))


def scaleDeployments(ns,sleepTime=None,replicas=None):
    """
    Function for scaling deployments
    """
    #Assign a default value if necessary
    if sleepTime == None:
        sleepTime = 10

    if replicas == None:
        replicas = 0

    getDeploymentCommand = "kubectl get deployment -n " + ns + " | grep -v NAME | awk '{print $1}'"

    tempDeploymentList = os.popen(getDeploymentCommand)
    tempDeploymentList = tempDeploymentList.read().split('\n')
    deploymentList = [deploy for deploy in tempDeploymentList if deploy]

    if len(deploymentList) > 0:
        print("\nDeployments for {0} namespace:\n{1}".format(ns,deploymentList))

        for deploymentItem in deploymentList:
            scaleCommand = "kubectl scale deployment " + deploymentItem + " -n " + ns + " --replicas=" + str(replicas)
            print(scaleCommand)
            scaleResult = os.popen(scaleCommand)
            print(scaleResult.read())
            #Sleep for a period to dial down the churn.
            time.sleep(int(sleepTime))


def scaleStatefulsets(ns,sleepTime=None,replicas=None):
    """
    Function for scaling deployments
    """
    #Assign a default value if necessary

    if sleepTime == None:
        sleepTime = 10

    if replicas == None:
        replicas = 0

    getDeploymentCommand = "kubectl get statefulsets -n " + ns + " | grep -v NAME | awk '{print $1}'"

    tempDeploymentList = os.popen(getDeploymentCommand)
    tempDeploymentList = tempDeploymentList.read().split('\n')
    deploymentList = [deploy for deploy in tempDeploymentList if deploy]

    if len(deploymentList) > 0:
        print("\nDeployments for {0} namespace:\n{1}".format(ns,deploymentList))

        for deploymentItem in deploymentList:
            scaleCommand = "kubectl scale statefulsets " + deploymentItem + " -n " + ns + " --replicas=" + str(replicas)
            print(scaleCommand)
            scaleResult = os.popen(scaleCommand)
            print(scaleResult.read())
            #Sleep for a period to dial down the churn.
            time.sleep(int(sleepTime))





def main():


    parser = argparse.ArgumentParser(
               description="Script for scaling pods\n")

    parser.add_argument('--type', required=True, default='deployments', action='store',
                           help='Deployments, Jobs or Statefulsets')


    parser.add_argument('--ns', required=False, action='store',
                           help='Namespace, single or comma delimited')

    parser.add_argument('--replicas', required=False, default="0", action='store',
                           help='repicas')

    parser.add_argument('--time', required=False, default="10", action='store',
                           help='Delay in between executions')


    config_args = parser.parse_args()

    #If a namespace isn't provided fetch them all
    if config_args.ns == None:
        nameSpacesList = getNamespaces()

    else:
        nameSpacesList = config_args.ns.split(',')


    for ns in nameSpacesList:

        if ns == "kube-system":
            print("\nLast chance to cancel before proceeding with kube-system deployments\n")
            time.sleep(30)

        print("Next Namespace: {}".format(ns))

        if config_args.type == "deployments":
            scaleDeployments(ns,config_args.time,config_args.replicas)

        if config_args.type == "jobs":
            scaleJobs(ns,config_args.time,config_args.replicas)

        if config_args.type == "statefulsets":
            scaleStatefulsets(ns,config_args.time,config_args.replicas)




if __name__ == "__main__":
    main()
