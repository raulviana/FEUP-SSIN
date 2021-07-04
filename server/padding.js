module.exports = {
    toB64padded: function(plaintext, blocksize){
        var bufPlaintext = Buffer.from(plaintext, 'utf8')
        var bufPlaintextB64 = Buffer.from(bufPlaintext.toString('base64'), 'utf8')      // Base64 encoding
        var bufPadding = Buffer.alloc(blocksize - bufPlaintextB64.length % blocksize)
        return Buffer.concat([bufPlaintextB64, bufPadding])                             // Zero padding
    },
    d2h: function(d) {
        var s = (+d).toString(16);
        if(s.length < 2) {
            s = '0' + s;
        }
        return s;
    }
}