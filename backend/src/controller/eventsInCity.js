import { User } from "../model/user.js"
//import * as cheerio from 'cheerio';

const eventsDatas = []
const eventsFindInCity = async function (req, res) {
    const { city } = req.body;
    //console.log(city);

    if (!city || city.trim() === "") {
        return res.status(400).json({
            success: false,
            message: "City is required"
        });
    }

    try {

        // Call FastAPI backend
        const response = await fetch('http://localhost:8000/fetch-city-events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ city }),
        });


        const result = await response.json();
        //console.log("✅ Events received from FastAPI:", result);
        //console.log("data from the python", result.data);
        if (!Array.isArray(result.data)) {
            console.error("❌ Expected array, got:", typeof result.data, result.data);
            return res.status(500).json({
                success: false,
                message: "Invalid data format from FastAPI"
            });
        }
        //const jsonResult = JSON.stringify(result.data)
        //console.log("jsonResult",jsonResult);

        return res.status(200).json({
            success: true,
            message: "City fetch successful",
            //jsonData:jsonResult,
            data: result.data
        });

    } catch (error) {
        console.error("❌ Error while calling FastAPI:", error.message);
        return res.status(500).json({
            success: false,
            message: "Error while calling FastAPI",
            error: error.message
        });
    }
};

const addUser = async (req, res) => {
    const { email } = await req.body;
    console.log(email);
    const user = await User.create({
        email
    })
    console.log(user);

    return res.status(201).json(
        {
            success: true,
            message: "User Register",
            data: user
        }
    )
}

export { eventsFindInCity, addUser };
