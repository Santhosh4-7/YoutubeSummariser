import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

function GenerateQuiz() {
    const location = useLocation();
    const sum = location.state || {}; // Ensure sum is defined
    const [questions, setQuestions] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        axios.post("http://localhost:3001/generate-quiz", { sum }) // Change to POST and send sum in body
            .then(response => {
                console.log(response.data);
                setQuestions(response.data.output); // Set the output from the response
            })
            .catch(err => {
                console.error(err);
            });
    }, [sum]);

    return (
        <div>
            <h4>{questions}</h4>
            <style>
                {`
                    body {
                        background: white;
                    }
                `}
            </style>
        </div>
    );
}

export default GenerateQuiz;
