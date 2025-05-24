import mongoose, { Schema } from "mongoose"


const eventSchema = new Schema({
    city: {
    type: String,
    required: true
  },
  title: {
    type: String,
  },
  dateTime: {
    type: String,
    required: true 
  },
  location: {
    type: String,
    required: true
  },
  price: {
    type: String,
    required: true // e.g., ₹1300, storing as string keeps the currency symbol
  },
  imageUrl: {
    type: String,
    required: true
  },
  link: {
    type: String,
    required: true // relative path or external link
  }
}, { timestamps: true })

export const Event = mongoose.model('Event', eventSchema);