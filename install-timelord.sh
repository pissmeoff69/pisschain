#!/usr/bin/env bash

set -o errexit

USAGE_TEXT="\
Usage: $0 [-d]

  -n                          do not install Python development package, Python.h etc
  -h                          display this help and exit
"

usage() {
  echo "${USAGE_TEXT}"
}

INSTALL_PYTHON_DEV=1

while getopts nh flag; do
  case "${flag}" in
  # development
  n) INSTALL_PYTHON_DEV= ;;
  h)
    usage
    exit 0
    ;;
  *)
    echo
    usage
    exit 1
    ;;
  esac
done

if [ -z "$VIRTUAL_ENV" ]; then
  echo "This requires the piss python virtual environment."
  echo "Execute '. ./activate' before running."
  exit 1
fi

echo "Timelord requires CMake 3.14+ to compile vdf_client."

PYTHON_VERSION=$(python -c 'import sys; print(f"python{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $PYTHON_VERSION"

if [ "$INSTALL_PYTHON_DEV" ]; then
  PYTHON_DEV_DEPENDENCY=lib"$PYTHON_VERSION"-dev
else
  PYTHON_DEV_DEPENDENCY=
fi

export BUILD_VDF_BENCH=Y # Installs the useful vdf_bench test of CPU squaring speed
THE_PATH=$(python -c 'import pathlib, pissvdf, importlib_resources; print(pathlib.Path(pissvdf.__file__).parent)')/vdf_client
# Note that this picks the version based on the requirement, not the presently
# installed pissvdf.
pissVDF_POETRY_INFO=$(.penv/bin/poetry show --no-ansi --no-interaction pissvdf)
echo "${pissVDF_POETRY_INFO}"
pissVDF_POETRY_INFO_VERSION=$(echo "${pissVDF_POETRY_INFO}" | grep 'version[[:space:]]*:' | sed 's/version[[:space:]]*: //')
echo "${pissVDF_POETRY_INFO_VERSION}"
pissVDF_VERSION="pissvdf==${pissVDF_POETRY_INFO_VERSION}"
echo "${pissVDF_VERSION}"

symlink_vdf_bench() {
  if [ ! -e vdf_bench ] && [ -e venv/lib/"$1"/site-packages/vdf_bench ]; then
    echo ln -s venv/lib/"$1"/site-packages/vdf_bench
    ln -s venv/lib/"$1"/site-packages/vdf_bench .
  elif [ ! -e venv/lib/"$1"/site-packages/vdf_bench ]; then
    echo "ERROR: Could not find venv/lib/$1/site-packages/vdf_bench"
  else
    echo "./vdf_bench link exists."
  fi
}

if [ "$(uname)" = "Linux" ] && type apt-get; then
  UBUNTU_DEBIAN=true
  echo "Found Ubuntu/Debian."

elif [ "$(uname)" = "Linux" ] && type dnf || yum; then
  RHEL_BASED=true
  echo "Found RedHat."

  if [ "$INSTALL_PYTHON_DEV" ]; then
    yumcmd="sudo yum install $PYTHON_VERSION-devel gcc gcc-c++ gmp-devel libtool make autoconf automake openssl-devel libevent-devel boost-devel python3 cmake -y"
  else
    yumcmd="sudo yum install gcc gcc-c++ gmp-devel libtool make autoconf automake openssl-devel libevent-devel boost-devel python3 cmake -y"
  fi

elif [ "$(uname)" = "Darwin" ]; then
  MACOS=true
  echo "Found MacOS."
fi

if [ -e "$THE_PATH" ]; then
  echo "$THE_PATH"
  echo "vdf_client already exists, no action taken"
else
  if [ -e venv/bin/python ] && test "$UBUNTU_DEBIAN"; then
    echo "Installing pissvdf dependencies on Ubuntu/Debian"
    # Install remaining needed development tools - assumes venv and prior run of install.sh
    echo "apt-get install libgmp-dev libboost-python-dev $PYTHON_DEV_DEPENDENCY libboost-system-dev build-essential -y"
    sudo apt-get install libgmp-dev libboost-python-dev "$PYTHON_DEV_DEPENDENCY" libboost-system-dev build-essential -y
    echo "Installing pissvdf from source on Ubuntu/Debian"
    echo venv/bin/python -m pip install --force --no-binary pissvdf "$pissVDF_VERSION"
    venv/bin/python -m pip install --force --no-binary pissvdf "$pissVDF_VERSION"
    symlink_vdf_bench "$PYTHON_VERSION"
  elif [ -e venv/bin/python ] && test "$RHEL_BASED"; then
    echo "Installing pissvdf dependencies on RedHat/CentOS/Fedora"
    # Install remaining needed development tools - assumes venv and prior run of install.sh
    echo "$yumcmd"
    ${yumcmd}
    echo "Installing pissvdf from source on RedHat/CentOS/Fedora"
    echo venv/bin/python -m pip install --force --no-binary pissvdf "$pissVDF_VERSION"
    venv/bin/python -m pip install --force --no-binary pissvdf "$pissVDF_VERSION"
    symlink_vdf_bench "$PYTHON_VERSION"
  elif [ -e venv/bin/python ] && test "$MACOS"; then
    echo "Installing pissvdf dependencies for MacOS."
    # The most recent boost version causes compile errors.
    brew install --formula --quiet boost@1.85 cmake gmp
    # boost@1.85 is keg-only, which means it was not symlinked into /usr/local,
    # because this is an alternate version of another formula.
    export LDFLAGS="-L/usr/local/opt/boost@1.85/lib"
    export CPPFLAGS="-I/usr/local/opt/boost@1.85/include"
    echo "Installing pissvdf from source."
    # User needs to provide required packages
    echo venv/bin/python -m pip install --force --no-binary pissvdf "$pissVDF_VERSION"
    venv/bin/python -m pip install --force --no-binary pissvdf "$pissVDF_VERSION"
    symlink_vdf_bench "$PYTHON_VERSION"
  elif [ -e venv/bin/python ]; then
    echo "Installing pissvdf from source."
    # User needs to provide required packages
    echo venv/bin/python -m pip install --force --no-binary pissvdf "$pissVDF_VERSION"
    venv/bin/python -m pip install --force --no-binary pissvdf "$pissVDF_VERSION"
    symlink_vdf_bench "$PYTHON_VERSION"
  else
    echo "No venv created yet, please run install.sh."
  fi
fi
echo "To estimate a timelord on this CPU try './vdf_bench square_asm 400000' for an ips estimate."
