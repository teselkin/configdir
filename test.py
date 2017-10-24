from configdir import ConfigDir

config = ConfigDir('example/config')
print(str(config.getall()))
print(str(config.get('debian')))
print(str(config.get('debian:debian')))
# print(str(config.get('debian:centos')))
# print(str(config.get('redhat:debian')))
print(str(config.get('redhat:centos')))
print(str(config.get('debian:debian:package_manager')))
