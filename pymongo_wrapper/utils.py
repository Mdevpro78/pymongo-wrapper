import pkgutil


def find_package(pkg_name):
    return pkgutil.find_loader(pkg_name) is not None

