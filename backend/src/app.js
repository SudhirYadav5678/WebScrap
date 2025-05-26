import express, { json, urlencoded } from "express"
import dotenv from "dotenv"
import cors from 'cors'
import eventsInCity from './routes/eventsInCity.js'



dotenv.config({
    path: './.env'
})

const app = express();

app.use(cors({
    origin: process.env.CORS_ORIGIN,
    credentials: true,

}))

app.use(json({ limit: "100kb" }))
app.use(urlencoded({ extended: true, limit: "16kb" }))
app.use(express.static('data'))


//router
app.use("/api/v1/", eventsInCity)
app.get("/",(req, res)=>{
    res.json("Server is live by Sudhir");
})

export { app }