let password = 'XJX2018@0102'
let code = require('./RSA_code')
let key = new code.RSAUtils.getKeyPair('10001', '', 'cc6bf6f00ea1c04effc401c58786e0bdba4bae48d29778fd0a05d98d8591a73c00b732bb7c8f7c803a06548ba7681f030d425f17939367f79ccbdea8673948785937717ab5819a1dd25a38d98260c667736b67b2e775befbab807f3f303589fa8c4e97f4f16c380331d79b66173056fbf12eff10b72abbbf32c53ea8809b1a5d')
let reversedPwd = password.split('').reverse().join('')
let encrypedPwd = code.RSAUtils.encryptedString(key, reversedPwd)
console.log(encrypedPwd)