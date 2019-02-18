import sys
import os
import platform
import argparse
import re

from log_helper import *

logger = setup_logger(name="qt_builder", level=logging.DEBUG, log_to_file=False)

# OS Flag
WINDOW_PLATFORM = 0
UNIX_PLATFORM = 1

# Pass install path as QTDIR value
QT_PRECONFIGURE_CMD = """SET QTDIR={0}
SET PATH=%QTDIR%\bin;%PATH%
SET QMAKESPEC=win32-msvc2010"""


# 1st param is archive file, 2nd is unpack path
P7UNZIP_COMMAND = "7z x -y {0} -o{1} -r"

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


def is_file_any(executable):
    """
    :param executable: Archiver executable file name
    :return: True if found in PATH, False otherwise
    """
    if not any([os.path.exists(os.path.join(p, executable)) for p in os.environ["PATH"].split(os.pathsep)]):
        return False
    return True


def is_7z_exist():
    """
    :return: True if 7zip is found
    """
    return is_file_any("7z.exe") or is_file_any("7z")


def unzip7(archive_file, unpack_path):
    """
    Use existing 7zip archiever to unpack 7z file
    :return: 7z.exe return code
    """
    unzip_file = P7UNZIP_COMMAND.format(archive_file, unpack_path)
    logger.info("Unzip file {0}".format(archive_file))
    logger.info(unzip_file)
    return os.system(unzip_file)


def get_target_cmd(target):
    """
    :param target: Either "x86" or "x64"
    :return: Second param is a switch for the script, generating development environment
    """
    if target == 'x64':
        return "/x64"
    elif target == 'x86':
        return "/x86"
    else:
        logger.error("Target should be either x86 or x64")


def set_windows_environment(cmd_shell, target_switch):
    """
    Set environment variables for Windows SDK 7.1 environment scripts
    :param cmd_shell: Ful path to cmd.exe, compatible with target architecture
    :param target_switch: "/x86" or "/x64"
    :return: Process return code
    """
    winsdk_script = "C:\\Program Files\\Microsoft SDKs\\Windows\\v7.1\\Bin\\SetEnv.Cmd"
    winsdk_environment = '''"{0}" /Release /x86 /win7'''.format(winsdk_script)

    # run SDK bat-file
    if not os.path.exists(winsdk_script):
        raise RuntimeError('Cannot detect Windows 7.1 SDK environment')
    logger.info('Setting Windows 7.1 SDK environment')

    cmd_process = "{0} /C {1}".format(cmd_shell, winsdk_environment)
    logger.info("Run setting environment: {0}".format(cmd_process))
    os.system(cmd_process)
    return 0


def set_unix_environment():
    """
    Read environment variables for the POSIX build
    :return:
    """
    raise NotImplementedError(set_unix_environment())


def run_configure(cmd_shell, install_path):
    variables_cmd = QT_PRECONFIGURE_CMD.format(install_path)
    configure_cmd = "configure.bat -prefix {0} {1}".format(install_path, QT_CONFIG_PARAMS)

    # TODO: run configure
    logger.info('Setting variables: {0}'.format(variables_cmd))
    logger.info('Run configure: {0}'.format(configure_cmd))


def get_dir_from_path(path_of_file):
    """
    Get current directory of specific path
    :param path_of_file:
    :return: The directory of a file string
    """
    if not os.path.exists(path_of_file):
        raise RuntimeError('Cannot detect Qt sources')
    return os.path.dirname(path_of_file)


def get_filename_from_path(path_of_file):
    """
    Get file name of specific path
    :param path_of_file:
    :return:
    """
    if not os.path.isfile(path_of_file):
        raise RuntimeError('{0} is not a file'.format(path_of_file))
    file = os.path.basename(path_of_file)
    file_name = re.search(r'(.+)\.(.+)$', file)
    return file_name.group(1)


def build_qt(qt_sources, qt_version, target, install_path):
    # 1. Unpack sources

    if not os.path.exists(qt_sources):
        raise RuntimeError('Cannot detect Qt sources')
    os.chdir(get_dir_from_path(qt_sources))
    logger.info("Current directory {0}".format(os.getcwd()))
    unzip_folder_path = get_filename_from_path(qt_sources)
    unzip7(qt_sources, unzip_folder_path)

    # 2. Set environment
    # target_switch = get_target_cmd(target)
    # set_windows_environment(target_switch)

    # TODO:
    # 3.Edit source code for x86
    # 4.Compile and install


def main():
    current_os = get_current_os()
    if current_os == WINDOW_PLATFORM:
        print("Start compiling")
    else:
        print("Compilation for {0} not implemented yet".format(platform.system()))
        return -1

    parser = argparse.ArgumentParser(description='Automatically building and installing qt framework')
    parser.add_argument('--qt-sources',
                        help='Path to Qt sources',
                        dest='qt_sources',
                        required=True)

    parser.add_argument('--qt-version',
                        help='Qt version to build, in format like 5.12.2',
                        dest='qt_version',
                        required=True)

    parser.add_argument('--target',
                        help='Qt target architecture, x86 or x64',
                        dest='target',
                        choices=['x86', 'x64'],
                        default='x64',
                        required=False)

    parser.add_argument('--install-path',
                        help='Path to install Qt directory, which contains bin, lib and include',
                        dest='install_path',
                        required=True)
    args = parser.parse_args()
    build_qt(args.qt_sources, args.qt_version, args.target, args.install_path)

    return 0


if __name__ == '__main__':
    sys.exit(main())
