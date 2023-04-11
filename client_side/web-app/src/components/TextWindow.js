import React from 'react';

function TextWindow({title, textArray, pageTitle}) {
  const textElements = textArray.map(text => {return <p>{text}</p>});
  return (
    <div className="comment text-module">
      <div className="window-title">
        {
          pageTitle == true ?
          <h2>{title}</h2>
          :
          <h3>{title}</h3>
        }
          <div>
            <button className="module-button">-</button>
            <button className="module-button">X</button>
          </div>
      </div>
      {textElements}
    </div>
  )
}

export default TextWindow;