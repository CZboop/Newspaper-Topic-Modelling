import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className='Navbar'>
        <ul>
            <li><Link to='/intro'>Introduction</Link></li>
        </ul>
    </nav>
  )
}

export default Navbar