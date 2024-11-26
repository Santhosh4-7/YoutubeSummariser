const mongoose = require('mongoose')

const UserSchema = new mongoose.Schema({
    Fname : String,
    Uname : String,
    email: String,
    pass: String,
})

const UserModel = mongoose.model("User",UserSchema)

module.exports = UserModel