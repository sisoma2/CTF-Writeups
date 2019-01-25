const crypto = require('crypto');

function decrypt(i, p) {

        const algorithm = 'aes-128-cbc';

        const key = crypto.scryptSync(p, 'salt', 16);
        const iv = Buffer.alloc(16, 0);

        const cipher = crypto.createDecipheriv(algorithm, key, iv);

        let result = cipher.update(i, 'hex', 'utf8');

        return cipher.final('utf8');
}

let arg = Buffer.from("MTI2NWVmNmJjY2RhYzc5OTg1MzhiOTBjOGYxMjVjZjk4M2RiN2ZmZjE3OGUzNWRlMDY4MWQzNDQzM2QxMWM2YQ==", 'base64').toString('ascii')
let flag = decrypt('c93ae864e1b525ab1c64a02e7996ea52', arg);
console.log("The flag is: " + flag);
