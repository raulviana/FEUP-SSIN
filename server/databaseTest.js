const sqlite3 = require('sqlite3').verbose();

// open the database
let db = new sqlite3.Database('../database/Database.db', sqlite3.OPEN_READWRITE, (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the database.');
});

let sql = `SELECT *
          FROM users`;

//get first result
db.get(sql, (err, row) => {
  if (err) {
    return console.error(err.message);
  }
  else if (row) {
    console.log(row.username);
    console.log(row.ip_address);
  }
});

function setIpAddress(username, ip){
  var sql_set_ip = "UPDATE users SET ip_address=? WHERE username=?";
  db.run(sql_set_ip, [ip, username], (err, row) => {
    if (err) {
      return console.error(err.message);
    }
    if (row) {
      console.log(row.username);
      console.log(row.ip_address);
    }
  });
}

setIpAddress("Pedro","127.0.0.1:9090");


db.close((err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Close the database connection.');
});
