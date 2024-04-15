import React from 'react';
import { ReactTyped } from "react-typed";
import './Message.css';

import terpUser from '../img/user_purple.svg';
import terpBot from '../img/bot.svg';

//https://uiball.com/ldrs/
import { grid } from 'ldrs'
grid.register()


const Message = ({ message, isAnimationComplete, setIsAnimationComplete}) => {
 
 const handleAnimationComplete = () => {
    if (message.isLast) {
      setIsAnimationComplete(true);
    }
 };
 console.log("Message text:", message.text, message.text === '...');

 return (
    <div className={`message ${message.type}`}>
      <div className="message-content">
      {message.text === '...' ? (
         <div style={{display:'flex', alignContent: 'center'}}>
            <l-grid
              size="25"
              speed="1.5" 
              color="white" 
            ></l-grid>
            <span style={{paddingLeft:'15px', fontSize:'15px'}}>
              <ReactTyped
                loop={true}
                strings={["Asking your advisor..."]}
                typeSpeed={30}
                backSpeed={30}
                showCursor={true}
                cursorChar="▐"
                onComplete={handleAnimationComplete}
              />
            </span>
          </div>
        ) : (
        !isAnimationComplete && message.isLast ? (
          <div style={{display:'flex', alignContent: 'center'}}>
            <l-grid
              size="25"
              speed="1.5" 
              color="white" 
            ></l-grid>
            <span style={{paddingLeft:'15px', fontSize:'15px'}}>
              <ReactTyped
                strings={[message.text]}
                typeSpeed={1}
                showCursor={true}
                cursorChar="▐"
                onComplete={handleAnimationComplete}
              />
            </span>
          </div>
            
        ) : (
          <div style={{display:'flex', alignItems:'flex-start'}}>
            <img src={message.type === 'bot' ? terpBot : terpUser} alt="Terp Logo" style={{width: "27px"}}/>

            <span style={{paddingTop:'3px', paddingLeft:'15px', fontSize:'15px'}}>
              <div dangerouslySetInnerHTML={{ __html: message.text }} />
            </span>
          </div>
            // <div dangerouslySetInnerHTML={{ __html: message.text }} />
        )
        )}
      </div>
    </div>
 );
};

export default Message;
