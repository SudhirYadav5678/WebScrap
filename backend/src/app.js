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

app.options('*', cors({
  origin: allowedOrigin,
  credentials: true
}));


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