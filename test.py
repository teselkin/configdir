from configdir import ConfigDir

config = ConfigDir(root='example/config')
config.open()
print(str(config.dict(keystr='debian:debian')))
print(str(config.get(keystr='debian:debian:package_manager')))
