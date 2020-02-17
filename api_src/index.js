const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const {Pool} = require('pg')
const crypto = require('crypto')

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: true,
});

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 8080;

var router = express.Router();
router.get('/ranking', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('select name, time from time order by time limit 10;')
    client.release();
    res.json(result.rows);
  } catch (err) {
    res.json({error: 'une erreur est survenue'})
  }
});

router.post('/register_run', async (req, res) => {
  try {
    let token = crypto.randomBytes(64).toString('hex');
    const client = await pool.connect();
    const result = await client.query('insert into run (token) values ($1);', [token])
    client.release();
    res.json({token: token});
  } catch (err) {
    res.json({error: 'une erreur est survenue'})
  }
});

router.post('/validate_run/:token/:name/:time', async (req, res) => {
  try {
    let token = req.params.token;
    let name = req.params.name;
    let time = req.params.time ;
    
    const client = await pool.connect();
    const result = await client.query('select * from run where token = $1;', [token])
    let valid = result.rows.length
    if (valid) {

      await client.query('delete from run where token=$1', [token]);
      await client.query('insert into time (name, time) values ($1, $2);', [name, time]);

      res.json({sucess: 'la run a été enregistrée !'})
      console.log("new time : " + name + " -> " + time)
    } else {
      res.json({error: 'la run n\'est pas valide'})
    }
  } catch (err) {
    res.json({error: 'une erreur est survenue', message: err})
  }
});

app.use('/', router);
app.listen(port);