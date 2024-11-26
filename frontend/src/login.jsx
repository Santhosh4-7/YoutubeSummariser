import { useState } from "react";
import axios from 'axios';
import { useNavigate, Link } from "react-router-dom";

function Login() {
    const [email, setEmail] = useState(''); // Initialize with empty string
    const [pass, setPass] = useState(''); // Initialize with empty string
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(email, pass);
        axios.post('http://localhost:3001/login', { email, pass })
            .then(result => {
                console.log(result);
                if (result.data === "Success") {
                    navigate('/home',{state:{email}});
                }
            })
            .catch(err => console.log(err));
    };

    return (
        <div className="wrapper">
            <form onSubmit={handleSubmit}>
                <h1>Login</h1>
                <div className="input-box">
                    <input 
                        type="email" 
                        placeholder="Username" 
                        onChange={(e) => setEmail(e.target.value)} 
                        required 
                    />
                    <i className='bx bxs-user'></i>
                </div>
                <div className="input-box">
                    <input 
                        type="password" 
                        placeholder="Password" 
                        onChange={(e) => setPass(e.target.value)} 
                        required 
                    />
                    <i className='bx bxs-lock-alt'></i>
                </div>
                <div className="remember-forgot">
                    <a href="#">Forgot-password?</a>
                </div>
                <button type="submit" className="btn">Login</button>
                <div className="register-link">
                    <p>Don't have an account? <Link to="/signup">Register</Link></p>
                </div>
            </form>

            <style>
                {`
                @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap");

                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: "Poppins", sans-serif;
                }

                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    background: url('/img.jpg') no-repeat;
                    background-size: cover;
                    background-position: center;
                }

                .wrapper {
                    width: 420px;
                    background: transparent;
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    backdrop-filter: blur(20px);
                    box-shadow: 0 0 10px rgba(0, 0, 0, .2);
                    color: #fff;
                    padding: 30px;
                    border-radius: 10px;
                }

                .wrapper h1 {
                    font-size: 36px;
                    text-align: center;
                }

                .wrapper .input-box {
                    width: 100%;
                    height: 50px;
                    margin: 30px 0;
                    position: relative;
                    background: transparent;
                }

                .input-box input {
                    width: 100%;
                    height: 100%;
                    background: transparent;
                    border: 2px solid rgba(255, 255, 255, 0.5);
                    outline: none;
                    border-radius: 40px;
                    font-size: 16px;
                    color: #fff;
                    padding: 0 45px 0 20px;
                }

                .input-box input::placeholder {
                    color: rgba(255, 255, 255, 0.7);
                }

                .input-box i {
                    position: absolute;
                    right: 20px;
                    top: 50%;
                    transform: translateY(-50%);
                    font-size: 20px;
                    color: white;
                }

                .wrapper .remember-forgot {
                    display: flex;
                    justify-content: space-between;
                    font-size: 14.5px;
                    margin: -15px 0 15px;
                }

                .remember-forgot label input {
                    accent-color: #fff;
                    margin-right: 3px;
                }

                .remember-forgot a {
                    color: #fff;
                    text-decoration: none;
                }

                .remember-forgot a:hover {
                    text-decoration: underline;
                }

                .wrapper .btn {
                    width: 100%;
                    height: 45px;
                    background: #fff;
                    border: none;
                    outline: none;
                    border-radius: 40px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 1);
                    cursor: pointer;
                    font-size: 16px;
                    color: #333;
                    font-weight: 600;
                }

                .wrapper .register-link {
                    font-size: 14.5px;
                    text-align: center;
                    margin: 20px 0 15px;
                }

                .register-link p a {
                    color: #fff;
                    text-decoration: none;
                    font-weight: 600;
                }

                .register-link p a:hover {
                    text-decoration: underline;
                }
                `}
            </style>
        </div>
    );
}

export default Login;
