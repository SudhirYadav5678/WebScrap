import { User } from "../model/user.js"
//import * as cheerio from 'cheerio';

const eventsDatas =[]
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

        //js web scarrping
        // const response = await fetch(`https://insider.in/all-events-in-${city}`)
        // if (!response.ok) {
        //     throw new Error(`FastAPI returned status ${response.status}`);
        // };
        // console.log(response.data);
        // const $ = cheerio.load(response.data);
        // const event =$("card-list-item");
        // event.each(function(){
        //     title = $(this).find("event_card_title").text();
        //     date_time =  $(this).find("event_card_date_string").text();
        //     location = $(this).find("event_card_location").text();
        //     price = $(this).find(".css-1sh8h77").text();
        //     image_tag = $(this).find("event_card_image").text();
        //     link_tag = $(this).find("a").text();

        //     eventsDatas.push({title,date_time,location,price,image_tag,link_tag})
        // })
        // console.log(eventsDatas);
        
        const result = await response.json();
        //console.log("✅ Events received from FastAPI:", result);
        //console.log("data from the python",result.data);
        
        const jsonResult = JSON.stringify(result.data)
        //console.log("jsonResult",jsonResult);
        
        return res.status(200).json({
            success: true,
            message: "City fetch successful",
            jsonData:jsonResult,
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

const addUser = async(req, res)=>{
    const {email} = await req.body;
    console.log(email);
    const user = await User.create({
        email
    })
    console.log(user);
    
    return res.status(201).json(
        {
            success: true,
            message: "User Register",
            data:user
        }
    )
}

export { eventsFindInCity,addUser };