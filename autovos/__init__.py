import sys
import os
import platform

from autovos.log_helper import *

WINDOW_PLATFORM = 0
UNIX_PLATFORM = 1

QT_CONFIG_PARAMS = "-mp -opensource -confirm-license -nomake tests -nomake examples -no-compile-examples" \
                   " -release -shared -pch -no-ltcg -accessibility -no-sql-sqlite -opengl desktop -no-openvg" \
                   " -no-nis -no-iconv -no-evdev -no-mtdev -no-inotify -no-eventfd -largefile -no-system-proxies" \
                   " -qt-zlib -qt-pcre -no-icu -qt-libpng -qt-libjpeg -qt-freetype -no-fontconfig -qt-harfbuzz" \
                   " -no-angle -incredibuild-xge -no-plugin-manifests -qmake -qreal double -rtti -strip -no-ssl" \
                   " -no-openssl -no-libproxy -no-dbus -no-audio-backend -no-wmf-backend -no-qml-debug -no-direct2d" \
                   " -directwrite -no-style-fusion -native-gestures -skip qt3d -skip qtactiveqt -skip qtandroidextras" \
                   " -skip qtcanvas3d -skip qtconnectivity -skip qtdeclarative -skip qtdoc -skip qtenginio" \
                   " -skip qtgraphicaleffects -skip qtlocation -skip qtmacextras -skip qtmultimedia" \
                   " -skip qtquickcontrols -skip qtquickcontrols2 -skip qtscript -skip qtsensors -skip qtserialbus" \
                   " -skip qtserialport -skip qtwayland -skip qtwebchannel -skip qtwebengine -skip qtwebsockets" \
                   " -skip qtwebview -skip qtx11extras -skip qtxmlpatterns"


def get_current_os():
    """
    Check current OS
    :return: OS code value
    """
    if os.name == 'nt':
        return WINDOW_PLATFORM
    elif os.name == 'posix':
        return UNIX_PLATFORM
    else:
        return -1


def main():
    current_os = get_current_os()
    if current_os == WINDOW_PLATFORM:
        print("Start compiling")
    else:
        print("Compilation for {0} not implemented yet".format(platform.system()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
