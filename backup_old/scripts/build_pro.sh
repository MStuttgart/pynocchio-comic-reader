#!/bin/bash
################################################################################
# Script for build pro files to Pynocchio Comic Reader
# Author: Michell Stuttgart
#-------------------------------------------------------------------------------
#
# This script will build a .pro files to Pynocchio Comic Reader
#-------------------------------------------------------------------------------
# USAGE:
#
# python setup.py build_pro or ./scripts/build_pro.sh
#
################################################################################

export Off=$'\e[0m'
export White=$'\e[1;37m'
export BlueBG=$'\e[1;44m'
export Yellow=$'\e[1;33m'

echo -e ""
echo -e " ${White}${BlueBG}                                                         ${Off}"
echo -e " ${White}${BlueBG}         -= Build .pro files =-                          ${Off}"
echo -e " ${White}${BlueBG}                                                         ${Off}"
echo -e ""

FILENAME='pynocchio.pro'

echo -e ""
echo -e "${Yellow} Start build ${FILENAME} file..."
echo -e "${Yellow} =-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ${Off}"
echo -e "${White}"

.venv/bin/pylupdate5 -verbose ${FILENAME}

if [ $? = 0 ]; then
    echo -e ""
    echo -e "${Yellow} Compile ${FILENAME} file successfully!!"
    echo -e "${Yellow} =-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ${Off}"
    echo -e ""
else
    echo -e ""
    echo -e "${Yellow} Compile ${FILENAME} file failed!!"
    echo -e "${Yellow} =-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ${Off}"
    echo -e ""
fi

echo -e ""