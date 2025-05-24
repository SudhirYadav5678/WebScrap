import { Router } from "express";
import { eventsFindInCity,addUser} from "../controller/eventsInCity.js";


const router = Router();

router.route('/eventsInCity').post(eventsFindInCity)
router.route('/addUser').post(addUser)


export default router