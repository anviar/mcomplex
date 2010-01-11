#/bin/sh

myLANG=ru
curDir="../locale/${myLANG}/LC_MESSAGES/"

mkdir -p ${curDir}
msgfmt ${myLANG}.po -o ${curDir}/mSSL.mo


