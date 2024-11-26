const mongoose = require('mongoose');

const summarySchema = new mongoose.Schema({
    email: String,
    videoUrl: String,
    summarizedText: String,},
    {timestamps:true}
);

const SummaryModel = mongoose.model("Summary",summarySchema);

module.exports = SummaryModel;
