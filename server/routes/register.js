const fs = require('fs');
var sha256 = require('js-sha256');
const forge = require('node-forge');
const express = require('express');
const Crypto = require('crypto');
const DB = require('../DBconnect');
let app = express.Router()
const utils = require("../utils")
const buffertrim = require('buffertrim') 
const symmetric = require('../symmetric_encryption')


function assymetric_decrypt (message){
    const pem = fs.readFileSync('../server/private.pem', 'utf8');
    const privateKey = forge.pki.decryptRsaPrivateKey(pem, '2210');
    return privateKey.decrypt(forge.util.decode64(message), 'RSA-OAEP', {
        md: forge.md.sha1.create(),
        mgf1: {
            md: forge.md.sha1.create()
        }
    });
}

app.get('/', function (req, res) {
    //console.log(req.body);
    res.download('../server/public.pem');
});

app.post('/get_token', function (req, res) {
    const now = Date.now()
    console.log("\nStart of Registration ...")
        
    // Check request lifetime
    const enc_time = req.body.time;
    const timeout = assymetric_decrypt(enc_time);
    if(Date.parse(timeout) + utils.TIMEOUT < now){
        console.log("Request lifetime expired.")
        res.status(500).json({"msg":"Request lifetime expired."})
        return
    }
    //console.log("(test) Request made", now - Date.parse(timeout), "ms ago.")

    const enc_ID = req.body.ID_encrypt;
    const enc_iv = req.body.encrypt_iv;
    const enc_key = req.body.encrypt_key;
    const username = req.body.username;
 
    // console.log("ID: " + enc_ID);
    // console.log("iv: " + enc_iv)
    // console.log("key: " + enc_key)
    
    const onetimeID = assymetric_decrypt(enc_ID);
    const iv = assymetric_decrypt(enc_iv);
    const symmetric_key = assymetric_decrypt(enc_key);
    // console.log("ID: " + onetimeID);
    // console.log("username: " + username);
    // console.log("key: " + symmetric_key);
    // console.log("iv: " + iv);
    console.log("... checking if username and one time id macthes DB")
    
    const sql_confirm_ID = "SELECT one_time_id FROM users WHERE username=?"
    //var stmt = DB.db.prepare(sql_confirm_ID);
    //stmt.get([username], (err, row) => {
    DB.db.get(sql_confirm_ID, [username], (err, row) => {
        if (err) {
            console.log("Error accessing database")
            return;
        } 
        else if (row == undefined) {
            console.log("Wrong username.\n")
            res.statusCode = 404;
            res.json({
                    'message': 'User not found',
            });
            return;
        }
        else {

            let onetimeIdHash = sha256(onetimeID)
            //console.log("SQL > " + row.one_time_id + '\n > Client > ' + sha256(onetimeID))
            if (row.one_time_id != onetimeIdHash) {
                console.log("Wrong one time ID.\n")
                res.statusCode = 401;
                res.json({
                    'message': 'Wrong one_time _ID',
                });
                return;
            }
            else {
                console.log("... valid username and one time id")

                //criar um token
                console.log("... creating token... ")
                const token = Crypto.randomBytes(12).toString('base64').slice(0, 12);
                //**************************************************************************** */
                
                const new_iv_server = symmetric.createNewIV(utils.SIZE)
                const enc_token = symmetric.encrypt( token, new_iv_server, symmetric_key)
                 res.statusCode = 200;
                res.json({
                    'token': enc_token,
                    'new_iv': new_iv_server
                });
                console.log("... saving new token and symmetric key in DB")
                utils.saveClientRegistration(username, token, symmetric_key);
                console.log("Registration done.\n")
            }  
        };
    });
});

module.exports = app
