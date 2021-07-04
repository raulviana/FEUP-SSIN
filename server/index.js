const express = require("express");

const auth = require('./routes/auth')
const service = require('./routes/service');
const register = require('./routes/register');
const coms = require('./routes/coms');

const app = express();
const port = 3000;

app.use(express.json());

app.use('/register', register);
app.use('/auth', auth)
app.use('/service', service);
app.use('/coms', coms);

app.listen(port, () =>
  console.log(`Server listening on port ${port}!`)
);