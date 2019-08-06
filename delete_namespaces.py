#!/usr/bin/python
import argparse
import os
import time
import sys


"""
Quick/dirty script for backing up a namespace before deleting it.
Arguments:
dir     Directory to backup configs to.
ns      Namespace to backup.
time    Amount of time to pause in between scaling executions.  Default is 10 seconds.
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


def backupNamespace(ns, backupDir,sleepTime):
    """
    Function for backup configurations
    """
    k8sObjects = ["cm", "ing", "secrets", "deployments", "statefulsets"]


    if not os.path.exists(backupDir):
        os.makedirs(backupDir)


    for k8sObj in k8sObjects:
        backupCommand = "kubectl get " + k8sObj + " -n " + ns + " -o yaml > " + backupDir + "/" + ns + "-" + k8sObj + ".yaml"
        print(backupCommand)
        backupResult = os.popen(backupCommand)
        print(backupResult.read())
        #Sleep for a period to dial down the churn.
        time.sleep(int(sleepTime))



def zipBackup(backupDir):
    """
    Zip backup
    """

    print("Backing up {0} now...".format(backupDir))
    try:
        zipCommand = "zip -r " + backupDir + ".zip" + " " + backupDir
        zipResult = os.popen(zipCommand)
        print(zipResult.read())
    except OSError as err:
        print("ERROR: {0}".format(err))
        sys.exit(1)

    print("zipped successfully...")



def getArgs():
    """
    fetch args
    """
    parser = argparse.ArgumentParser(
            description="Script for backing up and deleting namespaces\n")

    parser.add_argument('--dir', required=False, action='store',
                           help='directory for backup')

    parser.add_argument('--ns', required=True, action='store',
                           help='Namespace, single or comma delimited')

    parser.add_argument('--time', required=False, default="5",action='store',
                           help='Time to sleep in between intervals')



    config_args = parser.parse_args()

    return (config_args)


def main():


    config_args = getArgs()

    zipBackup(backupDir)
    sys.exit(0)

    #Variables for arguments
    nameSpacesList = config_args.ns.split(',')
    if config_args.dir == None:
        print("No backup directory was provided, using namespace")
        backupDir = config_args.ns
    sleepTime = config_args.time

    print(config_args.dir)

    for ns in nameSpacesList:

        if ns == "default" or ns == "dev" or ns == "kube-system" or ns == "prod" or ns == "qa" or ns == "staging" or ns == "uat":
            print("\nUnauthorized namespace selection: {0}\n".format(config_args.ns))
            sys.exit(0)


        print("Next Namespace: {}".format(ns))

        #Backup namespace
        backupNamespace(ns,backupDir,sleepTime)

        #Zip directory
        zipBackup(backupDir)






if __name__ == "__main__":
    main()

