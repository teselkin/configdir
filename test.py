from configdir import ConfigDir

config = ConfigDir(root='example/config')
config.open()
print(str(config.load(keystr='')))
print(str(config.load(keystr=':')))
print(str(config.load(keystr='debian:debian')))
print(str(config.get(keystr='debian:debian:package_manager')))
