import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Logo from './Logo';
import './styles/styles.css';

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="auth-container">
      <div className="auth-content">
        <div className="auth-form">
          <h2>{isLogin ? 'Login' : 'Sign Up'}</h2>
          <form>
            <div className="form-group">
              <label>Email</label>
              <input type="email" required />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input type="password" required />
            </div>
            {!isLogin && (
              <div className="form-group">
                <label>Confirm Password</label>
                <input type="password" required />
              </div>
            )}
            <button type="submit" className="auth-button">
              {isLogin ? 'Login' : 'Sign Up'}
            </button>
          </form>
          <p className="auth-toggle">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <span onClick={() => setIsLogin(!isLogin)}>
              {isLogin ? 'Sign Up' : 'Login'}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}

export default AuthPage;
