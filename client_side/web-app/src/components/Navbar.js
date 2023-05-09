import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import { useState, useEffect} from "react";

function Navbar() {
  const [navOpen, setNavOpen] = useState(false);

  const toggleNavOpen = () => {
    setNavOpen(!navOpen);
  }

  // setting state to close navbar on link click, should only affect on mobile/small screens
  const closeNavOnClick = () => {
    setNavOpen(false);
  }

  useEffect(() => {}, []);

  return (
    <nav className={navOpen ? "Navbar Navbar-open" : "Navbar"}>
        <span className="Navbar-title"><Link className="Nav-title-link" to="/home" onClick={()=>closeNavOnClick()}>📰 UK News Topic Modelling</Link></span>
        <div className='Nav-links'>
            <Link to='/intro' onClick={()=>closeNavOnClick()}><button className='nav-button highlighted-link'>Introduction</button></Link>
            <Link to='/guardian' onClick={()=>closeNavOnClick()}><button className='nav-button highlighted-link'>Guardian</button></Link>
            <Link to='/mirror' onClick={()=>closeNavOnClick()}><button className='nav-button highlighted-link'>Mirror</button></Link>
            <Link to='/metro' onClick={()=>closeNavOnClick()}><button className='nav-button highlighted-link'>Metro</button></Link>
            <Link to='/mail' onClick={()=>closeNavOnClick()}><button className='nav-button highlighted-link'>Daily Mail</button></Link>
            <Link to='/telegraph' onClick={()=>closeNavOnClick()}><button className='nav-button highlighted-link'>Telegraph</button></Link>
            <Link to='/sun' onClick={()=>closeNavOnClick()}><button className='nav-button highlighted-link'>Sun</button></Link>
            <Link to='/express' onClick={()=>closeNavOnClick()}><button className='nav-button highlighted-link'>Express</button></Link>
          </div>
        <button className={navOpen ? "burger burger-open" : "burger"} id="burger-toggle" onClick={()=>toggleNavOpen()}> 
          <div id="open-button">
            <svg xmlns="http://www.w3.org/2000/svg" className="icon" width="44" height="44" viewBox="0 0 24 24" strokeWidth="1.5" stroke="black" fill="black" strokeLinecap="round" strokeLinejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <line x1="4" y1="6" x2="20" y2="6" />
            <line x1="4" y1="12" x2="20" y2="12" />
            <line x1="4" y1="18" x2="20" y2="18" />
            </svg>
          </div>
          <div id="close-button">
            <svg xmlns="http://www.w3.org/2000/svg" className="icon" width="44" height="44" viewBox="0 0 24 24" strokeWidth="1.5" stroke="black" fill="rgb(75, 0, 125)" strokeLinecap="round" strokeLinejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
            <rect x="4" y="4" width="16" height="16" rx="2" />
            <path d="M10 10l4 4m0 -4l-4 4" />
            </svg>
          </div>
        </button>
        
    </nav>
  )
}

export default Navbar