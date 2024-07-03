// get the client
const mysql = require('mysql2/promise');

// db 연결 풀
const pool = mysql.createPool({
  host: 'aws 퍼블릭 ip',
  user: 'username',
  password: "pw",
  database: 'DB name',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

module.exports = pool