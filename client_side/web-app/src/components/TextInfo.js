import React from 'react';
import InfoIcon from './InfoIcon.js';

function TextInfo({textArray, title}) {
    const textElements = textArray.map((text, index) => {return <p key={index.toString()}>{text}</p>})
  return (
    <div className="boilerplate text-module">
        <InfoIcon />
        {
            title ?
            <h3>{title}</h3>
            :
            null
        }
        {textElements}
    </div>
  )
}

export default TextInfo