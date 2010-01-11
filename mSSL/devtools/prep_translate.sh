#/bin/sh

intltool-extract --type=gettext/glade ../mSSL.glade
xgettext -k_ -kN_ -o messages.pot ../mSSL.py ../mSSL.glade.h
rm ../mSSL.glade.h
msginit
rm messages.pot