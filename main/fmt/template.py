pkgname = "fmt"
pkgver = "10.2.1"
pkgrel = 1
build_style = "cmake"
configure_args = [
    "-DBUILD_SHARED_LIBS=ON",
]
# FIXME: random musl issues
# format hangs on ppc64
make_check_args = ["-E", "(format|chrono|unicode|xchar)"]
hostmakedepends = [
    "cmake",
    "ninja",
    "pkgconf",
    "python",
]
pkgdesc = "Formatting library for C++"
maintainer = "psykose <alice@ayaya.dev>"
license = "MIT"
url = "https://fmt.dev/latest/index.html"
source = (
    f"https://github.com/fmtlib/fmt/releases/download/{pkgver}/fmt-{pkgver}.zip"
)
sha256 = "312151a2d13c8327f5c9c586ac6cf7cddc1658e8f53edae0ec56509c8fa516c9"
# CFI: test failures
hardening = ["vis", "!cfi"]


def post_install(self):
    self.install_license("LICENSE")


@subpackage("fmt-devel")
def _devel(self):
    return self.default_devel()
