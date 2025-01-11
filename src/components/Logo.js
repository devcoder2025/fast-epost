import React from 'react';

const Logo = ({ src = "/logo_test.png", alt = "Fast ePost Logo" }) => (
  <img 
    src={src} 
    alt={alt} 
    className="logo" 
    style={{ width: '150px', height: 'auto', transition: 'transform 0.3s' }} 
    onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.1)'} 
    onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'} 
  />
);

export default Logo;
