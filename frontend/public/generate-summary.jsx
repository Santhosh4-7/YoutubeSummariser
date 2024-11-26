import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

function Gsum() {
    const location = useLocation();
    const url = location.state || {};
    const [sum, setSum] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        console.log("Posting URL:", url); // Log the URL being sent
        axios.post('http://localhost:3001/generate-summary', { url })
            .then(result => {
                console.log(result.data.output.toString());
                setSum(result.data.output.toString());
            })
            .catch(err => console.error("Error fetching summary:", err));
    }, [url]);
    

    const handleSubmit = (e) => {
        e.preventDefault();
        navigate('/generate-quiz', { state: { sum } });
    };

    return (
        <div className='gSum'>
            <h2>Url:</h2>
            <p>{url.url}</p>
            <br/>
            <h2>Summary:</h2>
            <p>{sum}</p>
            <form onSubmit={handleSubmit}>
                <button type='submit'>Generate quiz</button>
            </form>

            <style>
                {
                    `
                    body{
                        background:white;
                    }
                    `
                }
                
                
            </style>

            
        </div>
    );
}

export default Gsum;
