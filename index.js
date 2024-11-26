const express = require("express");
const mongoose = require("mongoose");
const cors = require('cors');
const UserModel = require('./models/Users');
const SummaryModel = require('./models/summary');
const {spawn} = require("child_process");
const path = require("path");


const app = express();
app.use(express.json());
app.use(cors());


mongoose.connect("mongodb://127.0.0.1:27017/YoutubeSummariser");


app.post("/login", (req, res) => {
    const { email, pass } = req.body;
    UserModel.findOne({ email: email })
        .then(user => {
            if (user) {
                if (user.pass === pass) {
                    res.json("Success");
                } else {
                    res.json("The password is incorrect");
                }
            } else {
                res.json("No record exists");
            }
        })
        .catch(err => res.status(500).json({ error: 'An error occurred during login' }));
});

app.post("/home", async (req, res) => {
    try {
        const email = req.body.email;
        const url  = req.body.url;
        const action = req.body.action;
        
        if(action === "summarise"){

        let summary = await SummaryModel.findOne({ videoUrl: url });
        if (!summary) {
            const scriptPath = path.join(__dirname, 'scripts', 'Summary_gen.py');
            const pythonProcess = spawn('python', [scriptPath, url]);

            pythonProcess.stdout.on('data', async (data) => {
                const summarizedText = data.toString();
                summary = await SummaryModel.create({ email, videoUrl: url, summarizedText });
                res.json({ output: summarizedText });
            });

            pythonProcess.stderr.on('data', (data) => {
                console.error(`stderr: ${data.toString()}`);
                res.status(500).json({ error: data.toString() });
            });
        } else {
            console.log(`Existing summary: ${summary.summarizedText}`);
            res.json({ summary: summary.summarizedText });
        }}else if(action == 'history'){
            
            let summary = await SummaryModel.find({email: email}).sort({createdAt:-1});
            console.log(summary);
            res.json(summary);
        }
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "An error occurred" });
    }
});

app.post('/generate-summary', (req, res) => {
    const { url } = req.body;
    console.log("Request URL:", url.url); // Log the incoming URL

    SummaryModel.findOne({ videoUrl: url.url })
        .then(summary => {
            if (summary) {
                console.log("Existing summary:", summary.summarizedText);
                res.json({ output: summary.summarizedText });
            } else {
                console.log("No summary found for this URL.");
                res.status(404).json({ error: "No summary found" });
            }
        })
        .catch(err => {
            console.error("Error occurred while fetching summary:", err);
            res.status(500).json({ error: "An error occurred while fetching summary" });
        });
});


app.post('/generate-quiz', (req, res) => {
    const {sum} = req.body; // Extract 'sum' from the body
    console.log(sum.sum);

    const scriptPath = path.join(__dirname, 'scripts', 'quiz.py');
    const pythonProcess = spawn('python', [scriptPath, sum.sum]);

    pythonProcess.stdout.on('data', (data) => {
        res.json({ output: data.toString() });
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        res.status(500).json({ error: data.toString() });
    });

    pythonProcess.on('close', (code) => {
        console.log(`python script finished with code ${code}`);
    });
});

app.post('/signup', (req, res) => {
    console.log(req.body);
    UserModel.create(req.body)
        .then(user => res.status(201).json(user))
        .catch(err => {
            console.error(err);
            res.status(500).json({ error: 'An error occurred' });
        });
});

app.listen(3001, () => {
    console.log("Server is running on port 3001");
});
