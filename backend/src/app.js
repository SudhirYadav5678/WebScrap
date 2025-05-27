import express, { json, urlencoded } from "express"
import dotenv from "dotenv"
import cors from 'cors'
import eventsInCity from './routes/eventsInCity.js'



dotenv.config({
    path: './.env'
})

const app = express();



const allowedOrigin = 'https://web-scrap-pi.vercel.app';

app.use(cors({
  origin: allowedOrigin,
  credentials: true,
  methods: ["GET", "POST", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization"]
}));

// Manual CORS preflight handler for all routes
app.options('*', (req, res) => {
  res.header('Access-Control-Allow-Origin', allowedOrigin);
  res.header('Access-Control-Allow-Methods', 'GET,POST,PUT,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.header('Access-Control-Allow-Credentials', 'true');
  res.sendStatus(204);
});


app.use(json({ limit: "100kb" }))
app.use(urlencoded({ extended: true, limit: "16kb" }))
app.use(express.static('data'))


//router
app.use("/api/v1/", eventsInCity)
app.get("/",(req, res)=>{
    res.send({
        "active":"True"
    });
})

export { app }