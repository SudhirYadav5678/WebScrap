import express, { json, urlencoded } from "express"
import dotenv from "dotenv"
import cors from 'cors'
import eventsInCity from './routes/eventsInCity.js'



dotenv.config({
    path: './.env'
})

const app = express();

const allowedOrigins = [
  'https://web-scrap-weld.vercel.app',
  'https://web-scrap-git-main-sudhiryadav5678s-projects.vercel.app',
];

app.use(cors({
  origin: function (origin, callback) {
    console.log('CORS check for origin:', origin);
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, origin);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
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