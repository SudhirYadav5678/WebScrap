import mongoose, { Schema } from "mongoose"


const userSchema = new Schema({
    email: {
        type: String,
        required: [true, "Email is required"],
        unique: [true, "Email most be unique"],
        trim: true
    },
}, { timestamps: true })

export const User = mongoose.model("User", userSchema);