#!/bin/bash
################################################################################
# Script for build of .deb package to Pynocchio Comic Reader
# Author: Michell Stuttgart
#-------------------------------------------------------------------------------
#
# This script will build a .deb package to Pynocchio Comic Reader
#-------------------------------------------------------------------------------
# USAGE:
#
# sh scripts/build_deb.sh
#
################################################################################

export Off=$'\e[0m'
export White=$'\e[1;37m'
export BlueBG=$'\e[1;44m'
export Yellow=$'\e[1;33m'

echo -e ""
echo -e " ${White}${BlueBG}                                                         ${Off}"
echo -e " ${White}${BlueBG}         -= Build .deb package =-                       ${Off}"
echo -e " ${White}${BlueBG}                                                         ${Off}"
echo -e ""

#--------------------------------------------------
# Define variables
#--------------------------------------------------

PACKAGE_VERSION=$1
BUILD_DEB_FOLDER="build_deb_package"
DIST='dist'
BUILD='build'
PACKAGE_NAME="pynocchio_${PACKAGE_VERSION}_amd64.deb"
CONTROL_FILE='linux/control'

#--------------------------------------------------
# Create the executable with PyInstaller
#--------------------------------------------------

rm -vrf ${BUILD}
rm -vrf ${DIST}
rm -vrf ${BUILD_DEB_FOLDER}

echo -e ""
echo -e "${Yellow} Run PyInstaller"
echo -e "${Yellow} =-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ${Off}"
echo -e "${White}"

pyinstaller pynocchio.spec

#--------------------------------------------------
# Create the package directory tree to .deb package
#--------------------------------------------------

# Change package version in html about file
sed -i -e "s:Version\: *.*.*:Version\: ${PACKAGE_VERSION}:g" ${CONTROL_FILE}

echo -e ""
echo -e "${Yellow} Create ${BUILD_DEB_FOLDER}/DEBIAN folder"
echo -e "${Yellow} =-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ${Off}"
echo -e "${White}"

mkdir -v -p ${BUILD_DEB_FOLDER}/DEBIAN

echo -e ""
echo -e "${Yellow} Create .deb package directory tree in ${BUILD_DEB_FOLDER}"
echo -e "${Yellow} =-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ${Off}"
echo -e "${White}"

mkdir -v -p ${BUILD_DEB_FOLDER}/usr/share
mkdir -v -p ${BUILD_DEB_FOLDER}/usr/bin
mkdir -v -p ${BUILD_DEB_FOLDER}/usr/share/pynocchio

echo -e ""
echo -e "${Yellow} Copy specific linux files to ${BUILD_DEB_FOLDER}"
echo -e "${Yellow} =-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ${Off}"
echo -e "${White}"

cp -v -r linux/applications ${BUILD_DEB_FOLDER}/usr/share/
cp -v -r linux/hicolor ${BUILD_DEB_FOLDER}/usr/share/
cp -v -r linux/pixmaps ${BUILD_DEB_FOLDER}/usr/share/
cp -v -r pynocchio/locale ${BUILD_DEB_FOLDER}/usr/share/pynocchio/

cp -v ${DIST}/* ${BUILD_DEB_FOLDER}/usr/bin
cp -v linux/control ${BUILD_DEB_FOLDER}/DEBIAN

echo -e ""
echo -e "${Yellow} Build ${PACKAGE_NAME} package"
echo -e "${Yellow} =-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ${Off}"
echo -e "${White}"

dpkg --build ${BUILD_DEB_FOLDER}/ ${PACKAGE_NAME}

#--------------------------------------------------
# Clean directory
#--------------------------------------------------

echo -e ""
echo -e "${Yellow} Remove ${BUILD}, ${DIST} and ${BUILD_DEB_FOLDER}"
echo -e "${Yellow} =-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ${Off}"
echo -e "${White}"

rm -vrf ${BUILD}
rm -vrf ${DIST}
rm -vrf ${BUILD_DEB_FOLDER}

echo -e ""
