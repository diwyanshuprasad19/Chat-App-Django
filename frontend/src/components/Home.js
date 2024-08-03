import React from 'react';
import '../css/Home.css';

function Home() {
  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Welcome to Our Website</h1>
        <p>Your one-stop solution for all your needs.</p>
      </header>
      <section className="home-content">
        <h2>About Us</h2>
        <p>
          We offer a wide range of services to help you achieve your goals. Whether you're looking for 
          technical solutions, professional services, or expert advice, we've got you covered.
        </p>
        <p>
          Our team of experienced professionals is dedicated to providing the best service possible. 
          Explore our website to learn more about what we have to offer.
        </p>
      </section>
    </div>
  );
}

export default Home;
