#!/usr/bin/python3.7
from amoCRM_update_lib import first_start
import pygsheets

if __name__ == '__main__':
    client_secret       = "JtNEdoLO72A4ZnpAN8aJivsKgwtnPsWRl1UavIEXHMcR56XCG01uJv2eAsglaPPo"
    client_id           = "531ea30d-da6a-4b2a-af04-d1118cf8692a"
    code                = 'def50200d5b82f3deba4bcefc392fe54854b973ef417bdcbbc47e55e11c2c379cdd921eb89421af7693611226f11453662b52471f281767a56301ab9b9b80d2426c6554613c5cce13c1de546f44c72df280a5fb01ac9c41ef18c7e253ad2b3d90812d4a416b89ab21174c3371bad73b795ba214517fd24cf760fa172d43d115bace8c65766b077d7fc9741e478902e0988a822c45ad8ffc7dfcf005b18932f374b1fcf21e1d97056622b84f4eba94a769b178386560bc5a20ce08c1f3bd7013b348fc1dbba8b3a6013eeaa7593f416e7bfd778d0efd89a1483939075a2161e3743c8307cb6bab4913669d7427a6954636103a44d092ee97c764f72b9bcb37d7b9d17eaa2c518eb76e9a8c7b8bf9c8cdc436cfa02331b0a19255923d06003fa4fb58c34683ce7aed2882c7d8b67fba9fd4697ca91736af188913a377bb28f66119f9453aa6deb76253896e8fd3c01b667f7652dc288e16d868b41e3dd3c1ba570ce756a0ea1abe9a979f7716e75db2de8f08929f512561cca9d1f0794defba3b7af6c1c1b9aaaa19c0a0fa82b15846d54e10af76365bc253c00fd892c3a427b29f06ae94fe7db51f741930259e1028cf5cd9f40c28305eea18fd45dcebe8d778db4169f6801805c41b998a2153787af04f80320c8e845963274fbb911141c77e933653b79b37e7255d11ffadea48a67bd2f8d540554eeb688348d7e541b312682b436da7df79e604c8a5a228c331f5237055c'
    url                 = "impactcapital.amocrm.ru"
    redirect_uri        = "https://docs.google.com/spreadsheets/d/12R1TPoXmAeGnR1azyWiG_jgpOG7tXibnGCDXXpqwpT4/edit?usp=sharing"
    filename            = url+'webhook'
    d                   = first_start(client_id, client_secret, code, redirect_uri,url, filename)

    print(d)


