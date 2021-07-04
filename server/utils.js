const sqlite3 = require('sqlite3');
const DBconnect = require('./DBconnect.js').db
const symmetric = require("./symmetric_encryption")
const TIMEOUT = 10000

/**
* Save token and symmetric key in DB
*
*/
function saveClientRegistration (username, token, symmetric_key) {
  const sql = "UPDATE users SET token=?, symmetric_key=? WHERE username=?"
  DBconnect.run(sql, [token, symmetric_key, username], async function (err, row) {
    if (err) {
      return console.error(err.message);
    }
  });
}

/**
* Save challenge and their expire timeout on the DB
*/
function saveChallenge (username, challenge, timeout) {
  const sql = "UPDATE users SET challenge=?, challenge_timeout=? WHERE username=?"
  DBconnect.run(sql, [challenge, timeout, username], async function (err, row) {
    if (err) {
      return console.error(err.message);
    }
  })
}

/**
* Save new token and ip_port of client session
*/
function saveClientNewSession (username, token) {
    const sql = "UPDATE users SET token=? WHERE username=?"
    DBconnect.run(sql, [token, username], async function (err, row) {
      if (err) {
        return console.error(err.message);
      }
    })
}

/**
 * Get client data from the DB with username
 */
function getOnlyClient(res, username, callback){
    const sql = `SELECT * FROM users WHERE username = "`+ username +'"'
    DBconnect.get(sql, (err, row) => {
        if (row == undefined){
          console.log("Authentication failed - User not found.")
          res.status(500).json({"msg":"User not found."})
        }
        else callback(row)
    })
}

/**
 * Get client data from the DB with username if token is correct and if the lifetime of the request is valid
 */
 function getClient(now, time, res, config, callback){
    const { username, cl_token, new_iv} = config

    const sql = `SELECT * FROM users WHERE username = "`+ username +'"'
    DBconnect.get(sql, (err, row) => {
        if (row == undefined){
          console.log("User not found.")
          res.status(500).json({"msg":"User not found."})
        }
        else{ 
            console.log("... checking lifetime request and if username and token macthes DB")
            
            // Check if username and token matches DB and request lifetime
            const { symmetric_key, token} = row

            // Check request lifetime
            const dec_time = symmetric.decrypt( time, new_iv, symmetric_key)
            if(Date.parse(dec_time) + TIMEOUT < now){
                console.log("Request lifetime expired.")
                res.status(500).json({"msg":"Request lifetime expired."})
                return
            }
            //console.log("(test) Request made", now - Date.parse(dec_time), "ms ago.")
           
            // Ckeck token
            const token_decrypted = symmetric.decrypt(cl_token, new_iv, symmetric_key)
            if(token != token_decrypted){
                console.log("Token do not macth this username.")
                res.status(500).json({"msg":"Token do not macth this username."})
                return
            }
            console.log("... valid username and token")
            callback(row)
        }
    })
}


module.exports = {
    saveClientRegistration,
    saveChallenge,
    saveClientNewSession,
    getOnlyClient,
    getClient,
    TIMEOUT
}