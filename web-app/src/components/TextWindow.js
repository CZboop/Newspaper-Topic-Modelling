import React from 'react';

// text window component for displaying main analysis text
function TextWindow({title, textArray, pageTitle}) {
  // mapping text array prop to paragraph elements
  const textElements = textArray.map((text, index) => {return <p key={index.toString()}>{text}</p>});
  return (
    <div className="comment text-module">
      <div className="window-title">
        {/* using ternary to alter size of title depending on pageTitle boolean - whether the window is acting as title for page or not */}
        {
          pageTitle === true ?
          <h2>{title}</h2>
          :
          <h3>{title}</h3>
        }
        <div>
          {/* buttons to be part of band at the top of window next to title */}
          <button className="module-button">-</button>
          <button className="module-button">X</button>
        </div>
      </div>
      {textElements}
    </div>
  )
}

export default TextWindow;