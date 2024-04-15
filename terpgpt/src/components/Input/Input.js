import React from 'react';
import TextareaAutosize from 'react-textarea-autosize';
import IconButton from '@mui/material/IconButton';
import Icon from '@mui/material/Icon';

import sendIcon from '../img/send.svg';
import './Input.css';

const Input = ({ inputValue, setInputValue, handleSendClick }) => (
  <div className="msgbox">
    <div className="inputarea">
      <TextareaAutosize
        minRows={1}
        maxRows={6}
        placeholder="What's on your mind..."
        className="input"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        style={{ color: 'white' }}
      />
    </div>
    <div className="sendbtn">
      <IconButton aria-label="icon button" onClick={handleSendClick}>
        <Icon>
          <img className="sendIcon" src={sendIcon} alt="Send Query"/>
        </Icon>
      </IconButton>
    </div>
  </div>
);

export default Input;