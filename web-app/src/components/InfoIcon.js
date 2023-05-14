import React from 'react';
import './InfoIcon.css';

// creating svg info 'i' icon to be used inside other components
function InfoIcon() {
  return (
    <div className="info-icon">
        <svg fill="#ffffff" width = "25px" height = "25px" version="1.1" viewBox="0 0 416.98 416.98" xmlSpace="preserve" xmlns="http://www.w3.org/2000/svg">  <path d="m356 61.156c-81.37-81.47-213.38-81.551-294.85-0.182-81.47 81.371-81.552 213.38-0.181 294.85 81.369 81.47 213.38 81.551 294.85 0.181 81.469-81.369 81.551-213.38 0.18-294.85zm-118.4 279.63c0 3.217-2.607 5.822-5.822 5.822h-46.576c-3.215 0-5.822-2.605-5.822-5.822v-172.9c0-3.217 2.607-5.822 5.822-5.822h46.576c3.215 0 5.822 2.604 5.822 5.822v172.9zm-29.11-202.88c-18.618 0-33.766-15.146-33.766-33.765 0-18.617 15.147-33.766 33.766-33.766s33.766 15.148 33.766 33.766c0 18.619-15.149 33.765-33.766 33.765z"/></svg>
    </div>
  )
}

export default InfoIcon;