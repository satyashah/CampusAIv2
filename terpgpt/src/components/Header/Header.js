import React from 'react';
import IconButton from '@mui/material/IconButton';
import Icon from '@mui/material/Icon';

import trashIcon from '../img/trash.svg';
import terpIcon from '../img/terp.svg';

import './Header.css';

const Header = ({ clearChatsAndLocalStorage }) => (
  <div className='header'>
    <div className='brand'>
      <img src={terpIcon} alt="Terp Logo" />
      <span>TerpGPT</span>
    </div>
    <IconButton aria-label="icon button" onClick={clearChatsAndLocalStorage}>
      <Icon>
        <img className="trashIcon" src={trashIcon} alt = "Delete Chats" />
      </Icon>
    </IconButton>
  </div>
);

export default Header;