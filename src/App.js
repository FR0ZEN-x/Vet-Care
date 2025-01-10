import React from 'react';
import './App.css';
import { HashRouter as Router, Routes, Route, Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home">
      <h1>Welcome to Vet Care</h1>
      <p>Your trusted partner in pet healthcare</p>
      <div className="services">
        <h2>Our Services</h2>
        <ul>
          <li>Regular Check-ups</li>
          <li>Vaccinations</li>
          <li>Emergency Care</li>
          <li>Pet Grooming</li>
        </ul>
      </div>
    </div>
  );
}

function About() {
  return (
    <div className="about">
      <h2>About Us</h2>
      <p>We are dedicated to providing the best care for your pets.</p>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="nav-menu">
          <Link to="/">Home</Link>
          <Link to="/about">About</Link>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 