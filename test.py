from configdir import ConfigDir

config = ConfigDir(root='example/config')
config.open()
print(str(config.load(keystr='')))
print(str(config.load(keystr=':')))
print(str(config.load(keystr='debian:debian')))
print(str(config.load(keystr='debian:centos')))
print(str(config.load(keystr='redhat:debian')))
print(str(config.load(keystr='redhat:centos')))
print(str(config.get(keystr='debian:debian:package_manager')))
