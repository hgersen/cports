pkgname = "zathura-pdf-poppler"
pkgver = "0.3.2"
pkgrel = 1
build_style = "meson"
hostmakedepends = ["meson", "pkgconf"]
makedepends = [
    "libpoppler-devel",
    "zathura-devel",
]
checkdepends = ["check-devel"]
depends = ["zathura"]
pkgdesc = "PDF support for zathura"
subdesc = "poppler backend"
maintainer = "ttyyls <contact@behri.org>"
license = "Zlib"
url = "https://pwmt.org/projects/zathura-pdf-poppler"
source = f"{url}/download/{pkgname}-{pkgver}.tar.xz"
sha256 = "71abeed51cd1d188cef3dbd4c164758e3c371604756967b23ad176ae53453011"


def post_install(self):
    self.install_license("LICENSE")
