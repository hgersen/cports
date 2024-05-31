pkgname = "accounts-qml-module"
# last release from previous century
pkgver = "0.7_git20231028"
pkgrel = 0
_gitrev = "05e79ebbbf3784a87f72b7be571070125c10dfe3"
build_style = "makefile"
make_cmd = "gmake"
make_use_env = True
hostmakedepends = [
    "gmake",
    "pkgconf",
    "qt6-qtbase",
]
makedepends = [
    "libaccounts-qt-devel",
    "qt6-qtdeclarative-devel",
    "signond-devel",
]
checkdepends = ["dbus-test-runner", "xserver-xorg-xvfb"]
pkgdesc = "QML bindings for signond/libaccounts-qt"
maintainer = "psykose <alice@ayaya.dev>"
license = "LGPL-2.1-only"
url = "https://gitlab.com/accounts-sso/accounts-qml-module"
source = f"https://gitlab.com/accounts-sso/accounts-qml-module/-/archive/{_gitrev}.tar.gz"
sha256 = "1a53a6d8a3a56694244bc24bdab844d91420483744822d08ae8517ff7df84763"

if self.profile().arch == "riscv64":
    broken = "qmake busted under emulation (https://bugreports.qt.io/browse/QTBUG-98951)"


def do_configure(self):
    # TODO: build style these
    self.do(
        "qmake6",
        "PREFIX=/usr",
        "CONFIG+=no_docs",
        f"QMAKE_CFLAGS={self.get_cflags(shell=True)}",
        f"QMAKE_CXXFLAGS={self.get_cxxflags(shell=True)}",
        f"QMAKE_LDFLAGS={self.get_ldflags(shell=True)}",
    )


def init_install(self):
    self.make_install_args += [f"INSTALL_ROOT={self.chroot_destdir}"]


def post_install(self):
    # mistakenly installed
    self.rm(self.destdir / "usr/bin/tst_plugin")
