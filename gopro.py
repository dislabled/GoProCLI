#!/usr/bin/python3

import os
import sys
import gptest
import argparse

parser = argparse.ArgumentParser(description='GoPro Command Line Tool')
parser.add_argument('-s', '--sync', help='Syncronize directory with gopro', required=False, type=bool)
parser.add_argument('-D', '--dryrun', help='Only print what to do', required=False, type=bool)
parser.add_argument('-F', '--format', help='Format SD Card', required=False, type=bool)
parser.add_argument('-d', '--download', help='Download all from SD Card', required=False, type=bool)
parser.add_argument('-o', '--out', help='Output path', default=".")
parser.add_argument('-t', '--time', help='Sync Computer time to GoPro', required=False, type=bool)
parser.add_argument('-l', '--listmedia', help='List Media on the GoPro', required=False, type=bool)
args = parser.parse_args()
gopro = gptest.GoProCamera.GoPro()
goproMedia = gopro.listMedia(format=True, media_array=True)  # goproMedia = ['directory', 'filename', 'filesize', 'timestamp']
#goproMedia = [['100GOPRO', 'GH010001.MP4', 111895657, 1577318564], ['100GOPRO', 'GH010002.MP4', 7407228, 1577319192], ['100GOPRO', 'GH010003.MP4', 40843873, 1577320466], ['100GOPRO', 'GH010004.MP4', 57722031, 1577320544]]


def localMedia():
    nameList = os.listdir(args.out)
    fsizes = [[] for _ in enumerate(nameList)]
    for n, f in enumerate(nameList):
        statinfo = os.stat(f)
        fileSize = statinfo.st_size
        fsizes[n].append(f)
        fsizes[n].append(str(fileSize))
    return fsizes


def convgplist():
    for n in range(len(goproMedia)):
        dir = goproMedia[n].pop(0)
        del goproMedia[n][2]
    return dir


def compareList():
    localmedia = localMedia()
    comparedList = [l for l in goproMedia if l not in localmedia]
    return comparedList


if args.sync:
    directory = convgplist()
    comparelist = compareList()
    if comparelist == []:
        print("All caught up!")
    else:
        for media in comparelist:
            if "MP4" or "JPG" or "RAW" in media[0]:
                newpath = args.out + "/" + media[0]
                if args.dryrun:
                    print("downloading: " + str(media[0]))
                else:
                    gopro.downloadMedia(directory, media[0], newpath)
        

if args.format:
    choice = input('{:5} (y/N)'.format('Are you sure you want to format? ')).lower() == 'y'
    if choice:
        if args.dryrun:
            print('Formatting SD Card')
        else:
            gopro.delete('all')

if args.time:
    gopro.syncTime()

if args.listmedia:
    for list in goproMedia:
        print('file:{} size:{}'.format(list[0], list[1]))
