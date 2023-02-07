import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className='Navbar'>
        <span className="Navbar-title"><Link className="Nav-title-link" to="/home">📰 UK News Topic Modelling</Link></span>
        <ul className='Nav-links'>
            <li className='highlighted-link'><Link to='/intro'>Introduction</Link></li>
            <li className='highlighted-link'><Link to='/guardian'>The Guardian</Link></li>
            <li className='highlighted-link'><Link to='/mirror'>The Mirror</Link></li>
            <li className='highlighted-link'><Link to='/metro'>Metro</Link></li>
            <li className='highlighted-link'><Link to='/mail'>Daily Mail</Link></li>
            <li className='highlighted-link'><Link to='/telegraph'>Telegraph</Link></li>
            <li className='highlighted-link'><Link to='/sun'>Sun</Link></li>
            <li className='highlighted-link'><Link to='/express'>Express</Link></li>
        </ul>
    </nav>
  )
}

export default Navbar