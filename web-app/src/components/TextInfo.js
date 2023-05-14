import React from 'react';
import InfoIcon from './InfoIcon.js';

// text info component - a text module with an info icon to be used for general info rather than analysis
function TextInfo({textArray, title}) {
  // mapping text items passed in via textArray prop to paragraph elements
  const textElements = textArray.map((text, index) => {return <p key={index.toString()}>{text}</p>})
  return (
    <div className="boilerplate text-module">
        <InfoIcon />
        {
          // making title optional with ternary, adding h3 if title prop present
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