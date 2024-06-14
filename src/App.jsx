import React from 'react'
import Component1 from './component'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router >
      <Routes>
        <Route exact path='/' Component={Component1} />
        <Route exact path='/123' Component={Component1} />
      </Routes>
    </Router>
  )
}

export default App