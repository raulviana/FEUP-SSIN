const sqlite3 = require('sqlite3');

/**
* Open the database
*/
let db = new sqlite3.Database('../database/Database.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
      console.error(err.message);
    }
    else console.log('Connected to database.');
  });


module.exports = {
  db
}