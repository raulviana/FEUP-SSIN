const padding = require('./padding')
const crypto = require('crypto');
const buffertrim = require('buffertrim') 

module.exports = {

    createNewIV: function(size, key){
        return crypto.randomBytes(8).toString('hex')
    },
    encrypt: function(message, iv, key) {
        var bufPlaintextB64padded = padding.toB64padded(message, 16)                              // Base64 encoding and Zero padding
        var cipher = crypto.createCipheriv('aes-128-cbc', key, iv)
        cipher.setAutoPadding(false)                                                        // Disable PKCS7 padding

        var ciphertextB64 = cipher.update(bufPlaintextB64padded, '', 'base64')              // Encryption, Base64 encoding of ciphertext 
        ciphertextB64 += cipher.final('base64')
        return ciphertextB64
    },
    decrypt: function(message,iv, key) {
        //console.log("message: " +message)

        var decipher = crypto.createDecipheriv('aes-128-cbc', key, iv)
        decipher.setAutoPadding(false)                                                      // Disable PKCS7 (un-) padding

        var bufPlaintextB64padded = Buffer.concat([                                         // Base64 decoding of ciphertext, decryption
            decipher.update(message, 'base64'), 
            decipher.final()
        ]);                                                                                 
        var bufPlaintextB64 = buffertrim.trimEnd(bufPlaintextB64padded)  
        return bufPlaintextB64.toString()
    }
};
