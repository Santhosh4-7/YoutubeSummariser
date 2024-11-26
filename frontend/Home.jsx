import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import './Home.css';
import { Link } from 'react-router-dom';

function Home() {
    const location = useLocation();
    const email = location.state.email || {};
    const navigate = useNavigate();
    const [url, setUrl] = useState("");
    const [sumArr, setSumArr] = useState([]);

    // Fetch old summaries
    useEffect(() => {
        axios.post('http://localhost:3001/home', { email, url: " ", action: "history" })
            .then(result => {
                setSumArr(result.data);
            }).catch(err => {
                console.error(err);
            });
    }, [email]);

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://localhost:3001/home', { email, url, action: "summarise" })
            .then(result => {
                navigate('/generate-summary', { state: { url } });
            })
            .catch(err => {
                console.error(err);
                alert("Failed to fetch summary. Please check the URL or try again later.");
            });
    };

    // Use effect to handle parallax on scroll
    useEffect(() => {
        const handleScroll = () => {
            let value = window.scrollY;
            document.getElementById('stars').style.left = value * 0.25 + 'px';
            document.getElementById('moon').style.top = value * 1 + 'px';
            document.getElementById('mountains_behind').style.top = value * 0.5 + 'px';
            document.getElementById('mountains_front').style.top = value * 0 + 'px';
            document.getElementById('text').style.marginRight = value * 4 + 'px';
            document.getElementById('text').style.marginTop = value * 1.5 + 'px';
            document.querySelector('header').style.top = value * 0.25 + 'px';
        };

        window.addEventListener('scroll', handleScroll);
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    return (
        <div>
            <header>
                <a href="#" className="logo">ClipCrushers</a>
            </header>

            <input type="checkbox" id="check" />
            
            <div id='sidebar'>
              {sumArr.map((item, index) => (
                <div key={index}>
                  <h2>Date:{new Date(item.createdAt).toLocaleDateString()}</h2>
                  <p>Url:{item.videoUrl}</p>
                  <Link to="/generate-summary" state={{ url: item.videoUrl }}>
                    <p>Summary:{item.summarizedText.split(" ").slice(0, 5).join(" ") + "..."}</p>
                  </Link>
                  <br></br>
                </div>
              ))}
            </div>

            <section>
                <img src="stars.png" id="stars" alt="stars" />
                <img src="youtube.png" id="moon" alt="moon" />
                <img src="mountains_behind.png" id="mountains_behind" alt="mountains behind" />
                <h2 id="text">YouTube Summariser</h2>
                <img src="mountains_front.png" id="mountains_front" alt="mountains front" />
            </section>

            <div className="sec" id="sec">
                <h2>Summarize a Video</h2>
                <form onSubmit={handleSubmit}>
                    <input type="text" name="url" placeholder="  Enter YouTube URL" onChange={(e) => setUrl(e.target.value)} required />
                    <button type="submit">Summarize</button>
                </form>
            </div>
        </div>
    );
}

export default Home;
