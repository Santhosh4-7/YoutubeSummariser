import Login from './login.jsx'
import Signup from './signup.jsx'
import Home from './Home.jsx'
import Gsum from './generate-summary.jsx'
import GenerateQuiz from './generate-quiz.jsx'
import {Routes, Route, BrowserRouter, Navigate} from 'react-router-dom'


function App() {
  return(
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Navigate to='/login'/>}/>
        <Route path='/login' element={<Login/>}></Route>
        <Route path='/Signup' element={<Signup/>}></Route>
        <Route path='/home' element={<Home/>}></Route>
        <Route path='/generate-summary' element={<Gsum/>}></Route>
        <Route path='/generate-quiz' element={<GenerateQuiz/>}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
 