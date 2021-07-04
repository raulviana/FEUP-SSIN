const Crypto = require("crypto")
const express = require("express")
let app = express.Router()
const net = require("net")
const symmetric = require("../symmetric_encryption")
const DB = require("../DBconnect.js")
const utils = require("../utils")

/**
 * A client sends their username+token, and is asking to start a new session
 * If username+token exists, Authenticator Server sends a challenge (different each time)
 */
app.get("/", function (req, res) {
    const now = Date.now()
    const { username, time } = req.body

    console.log("Start of authentication ...")
    console.log("... client: " + "I'm username " + username)

    utils.getClient(now, time, res, req.body, (client) => {
      // Generate challenge, a unique random value
      const N = Crypto.randomBytes(32).toString("hex")

      // (slides) Protecting against replays needs a nonce or a timestamp
      // (slides) Timestamps need time synchronization which enlarges the attack surface
      // The challenge has a challenge timeout that expires
      const expire_time = Date.now() + utils.TIMEOUT

      // Save challenge on the DB, and its expire timeout
      utils.saveChallenge(username, N, expire_time, client.symmetric_key)

      // Encrypt timeout and msg
      const new_iv_server = symmetric.createNewIV(utils.SIZE)
      const enc_msg = symmetric.encrypt( username+ "? Prove it, a challenge was sent.", new_iv_server, client.symmetric_key)

      res.status(200).json({"msg": enc_msg, challenge: N, new_iv: new_iv_server})

    })
})

/**
 * Client challenge asnwer
 * If client is correct, refresh token
 */
app.get("/challengeRefreshToken", function (req, res) {
  const now = Date.now()
  const { username, enc_challenge, ip_port, new_iv, time} = req.body
  console.log("... client: Challenge solved")

  // Verify if is correct
  // Get symmetric key and encrypted challenge from DB, + timeout
  utils.getOnlyClient(res, username, (client) => {
    const { challenge, challenge_timeout, symmetric_key } = client

    // Check request lifetime
    const timeout_res = symmetric.decrypt( time, new_iv, client.symmetric_key)
    if(Date.parse(timeout_res) + utils.TIMEOUT < now){
      console.log("Request lifetime expired.")
      res.status(500).json({"msg":"Request lifetime expired."})
      return
    }
    //console.log("(test) Request made", now - Date.parse(timeout_res), "ms ago.")

    // Check challenge lifetime
    if(challenge_timeout < now){
      console.log("Authentication failed - challenge lifetime expired.")
      res.status(500).json({"msg":"Challenge lifetime expired."})
      return
    }
    //console.log("(test) callhenge lifetime finishes in", challenge_timeout - now, "ms.")

    // Decrypt challenge answer 
    const dec_challenge = symmetric.decrypt(enc_challenge, new_iv, symmetric_key)
    // Encrypted challenge from DB must be equal to answer: enc_challenge
    if(challenge != dec_challenge){
      console.log("Authentication failed - answer do not macth.")
      res.status(500).json({"msg":"Answer do not macth."})
      return
    }

    // (slides) If so, distribute a short-term session key(new token) for being used between the two
    // Create new token
    const new_token = Crypto.randomBytes(12).toString("base64").slice(0, 12)
            
    // Update DB with new token of client session
    utils.saveClientNewSession (username, new_token)

    // Encrypt new token and msg
    const new_iv_server = symmetric.createNewIV(utils.SIZE)
    const enc_msg = symmetric.encrypt("Okay, it is a match.", new_iv_server, symmetric_key)
    const enc_token = symmetric.encrypt( new_token, new_iv_server, symmetric_key)

    console.log("... creating new token, update port in DB")

    // Send new token to the client
    res.status(200).json({"msg":enc_msg, token: enc_token, "new_iv": new_iv_server})
    console.log("Authentication done.\n")
  })
})

module.exports = app