import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className='Navbar'>
        <ul>
            <li><Link to='/intro'>Introduction</Link></li>
            <li><Link to='/guardian'>The Guardian</Link></li>
            <li><Link to='/mirror'>The Mirror</Link></li>
            <li><Link to='/metro'>Metro</Link></li>
            <li><Link to='/mail'>Daily Mail</Link></li>
            <li><Link to='/telegraph'>Telegraph</Link></li>
            <li><Link to='/sun'>Sun</Link></li>
            <li><Link to='/express'>Express</Link></li>
        </ul>
    </nav>
  )
}

export default Navbar