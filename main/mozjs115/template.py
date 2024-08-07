pkgname = "mozjs115"
pkgver = "115.13.0"
pkgrel = 1
make_cmd = "gmake"
hostmakedepends = [
    "cargo",
    "gawk",
    "gm4",
    "gmake",
    "perl",
    "pkgconf",
    "python",
    "rust",
]
makedepends = [
    "icu-devel",
    "libedit-devel",
    "libffi-devel",
    "linux-headers",
    "nspr-devel",
    "rust-std",
    "zlib-ng-compat-devel",
]
pkgdesc = "Mozilla JavaScript interpreter and library, version 115.x"
maintainer = "q66 <q66@chimera-linux.org>"
license = "MPL-2.0"
url = "https://www.mozilla.org/firefox"
source = f"$(MOZILLA_SITE)/firefox/releases/{pkgver}esr/source/firefox-{pkgver}esr.source.tar.xz"
sha256 = "3fa20d1897100684d2560a193a48d4a413f31e61f2ed134713d607c5f30d5d5c"
tool_flags = {"LDFLAGS": ["-Wl,-z,stack-size=1048576"]}
env = {
    "MACH_BUILD_PYTHON_NATIVE_PACKAGE_SOURCE": "system",
    "RUST_TARGET": self.profile().triplet,
    "PYTHON": "/usr/bin/python3",
    "SHELL": "/usr/bin/sh",
    "MAKE": "gmake",
    "AWK": "gawk",
    "M4": "gm4",
    # firefox checks for it by calling --help
    "CBUILD_BYPASS_STRIP_WRAPPER": "1",
}
# FIXME int (fails basic/hypot-approx.js)
hardening = ["!int"]
# dependencies are not crossable for now and it's probably tricky
options = ["!cross"]


def init_configure(self):
    from cbuild.util import cargo

    self.env["MOZBUILD_STATE_PATH"] = str(self.chroot_srcdir / ".mozbuild")
    self.env["AS"] = self.get_tool("CC")
    self.env["MOZ_MAKE_FLAGS"] = f"-j{self.make_jobs}"
    self.env["MOZ_OBJDIR"] = f"{self.chroot_cwd / 'objdir'}"
    self.env["RUST_TARGET"] = self.profile().triplet
    # use all the cargo env vars we enforce
    self.env.update(cargo.get_environment(self))


def do_configure(self):
    self.rm("objdir", recursive=True, force=True)
    self.mkdir("objdir")

    extra_opts = []

    match self.profile().arch:
        case "x86_64" | "aarch64":
            extra_opts += ["--disable-elf-hack"]

    if self.has_lto():
        extra_opts += ["--enable-lto=cross"]

    self.do(
        "python3",
        self.chroot_cwd / "mach",
        "configure",
        "--prefix=/usr",
        "--libdir=/usr/lib",
        "--host=" + self.profile().triplet,
        "--target=" + self.profile().triplet,
        "--enable-application=js",
        "--enable-linker=lld",
        "--enable-release",
        "--enable-hardening",
        "--enable-optimize",
        "--disable-install-strip",
        "--disable-strip",
        # system libs
        "--with-system-zlib",
        "--with-system-nspr",
        "--with-system-icu",
        # features
        "--enable-tests",
        "--enable-ctypes",
        "--enable-readline",
        "--enable-shared-js",
        "--enable-system-ffi",
        "--with-intl-api",
        # disabled features
        "--disable-jemalloc",
        "--disable-debug",
        # conditional opts
        *extra_opts,
        wrksrc="objdir",
    )


def do_build(self):
    self.do(
        "python3",
        self.chroot_cwd / "mach",
        "build",
        "--priority",
        "normal",
        wrksrc="objdir",
    )


def do_install(self):
    self.do(
        "gmake", "-C", "objdir", "install", f"DESTDIR={self.chroot_destdir}"
    )


def post_install(self):
    self.uninstall("usr/lib/libjs_static.ajs")
    # it has correct soname but not the right file name
    self.rename("usr/lib/libmozjs-115.so", "libmozjs-115.so.0")
    self.install_link("usr/lib/libmozjs-115.so", "libmozjs-115.so.0")


def do_check(self):
    self.do("objdir/dist/bin/jsapi-tests")


@subpackage("mozjs115-devel")
def _devel(self):
    # include the interactive interpreter
    return self.default_devel(extra=["usr/bin"])
