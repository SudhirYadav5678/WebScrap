import dotenv from "dotenv"
import { app } from "./app.js"
import { dbConnect } from "./utiles/dbConnection.js"


// Load environment variables
dotenv.config({
    path: './.env'
})

dbConnect().catch((err) => {
    console.log("Server connection failed !!! ", err);
});

// For Vercel: export the Express app as default (do not call listen)
export default app;

// For local development, you can use a separate script to call app.listen if needed.