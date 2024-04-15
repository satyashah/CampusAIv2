import React, { useState, useEffect } from 'react';
import './App.css';

import Message from './components/Message/Message';
import Input from './components/Input/Input';
import Header from './components/Header/Header';

import api from './components/Backend/axiosConfig';

// function renderSafeHTML(htmlString) {
//   const div = document.createElement('div');
//   div.textContent = htmlString;
//   return div.innerHTML;
// }

function App() {
  const [isAnimationComplete, setIsAnimationComplete] = useState(true);

  const [inputValue, setInputValue] = useState("");

  const [messages, setMessages] = useState(() => {
    const savedMessages = window.localStorage.getItem('messages');
    return savedMessages ? JSON.parse(savedMessages) : [];
  });

  useEffect(() => {
    window.localStorage.setItem('messages', JSON.stringify(messages));
  }, [messages]);

  const clearChatsAndLocalStorage = () => {
    setMessages([]);
    window.localStorage.clear();
  };
  
  const handleSendClick = () => {

    setMessages(prevMessages => {
      const newMessages = [...prevMessages];
      newMessages[newMessages.length - 1] = {...newMessages[newMessages.length - 1], isLast: false};
      newMessages.push({ text: inputValue.replace(/\n/g, '<br>'), type: 'user' }, {text: '...', type: 'bot', isLast: true });
      return newMessages;
    });

    if (!inputValue.trim()) {
      alert("Please enter a message."); // Alert if empty message
      return; // Don't send empty messages
    }

    console.log("Sending:", inputValue);
    api.post('/askGPT', { "content": {messages, inputValue} })
    .then(response => 
      {
        const botResponse = response.data.result;
        console.log("Bot Response:", botResponse);
        updateMessages(botResponse);
      })
    .catch(error => 
      {
        const botResponse = "Sorry, I am not able to process your request at the moment. Please try again later.";
        console.log("Bot Response:", botResponse);
        updateMessages(botResponse);
      });


    setInputValue("");  
  };

  const updateMessages = (botResponse) => {
    setMessages(prevMessages => {
      const newMessages = [...prevMessages];
      newMessages[newMessages.length - 1] = {...newMessages[newMessages.length - 1], text: botResponse.replace(/\n/g, '<br>'), isLast: true};
      return newMessages;
    });
    setIsAnimationComplete(false);
    

    setInputValue("");
 };


  return (
    <div className='App'>
      
      <Header clearChatsAndLocalStorage={clearChatsAndLocalStorage} />
      
      <div className="uppersection">
        {messages.map((message, index) => (
          <Message key={index} message={message} isAnimationComplete={isAnimationComplete} setIsAnimationComplete={setIsAnimationComplete} />
        ))}
      </div>
      
      <div className="lowersection">
        <Input inputValue={inputValue} setInputValue={setInputValue} handleSendClick={handleSendClick} />
        <div style={{display: "flex", color: "gray", fontSize: "13px", justifyContent: "center", paddingTop: "5px"}}>
          <span>TerpGPT can make mistakes. Consider checking important information.</span></div>
      </div>
    </div>
  );
}

export default App;