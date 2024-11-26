import { useState } from "react";
import axios from 'axios'
import { useNavigate } from "react-router-dom";

function Signup(){

    const [Fname, setFName] = useState()
    const [Uname, setUName] = useState()
    const [email, setEmail] = useState()
    const [pass, setPass] = useState()
    const navigate = useNavigate()

    const handleSubmit = (e) => {
        console.log(email,pass,Uname,Fname)
        e.preventDefault()
        axios.post('http://localhost:3001/signup',{Fname,Uname,email,pass})
        .then(result => {console.log(result)
        navigate('/login')
        })
        .catch(err => console.log(err))
        }

    return(
        <div>
             <form onSubmit = {handleSubmit}>
            <div>
            <input type="text" placeholder="FullName" onChange={(e)=>setFName(e.target.value)} required/>
            </div>
            <div>
            <input type="text" placeholder="UserName" onChange={(e)=>setUName(e.target.value)} required/>
            </div>
            <div>
            <input type="email" placeholder="Email Id" onChange={(e)=>setEmail(e.target.value)} required/>
            </div>
            <div>
            <input type="password" placeholder="Password" onChange={(e)=>setPass(e.target.value)} required/>
            </div>
            <button type="submit">SignUp</button>
            </form>
        </div>
    )
}

export default Signup