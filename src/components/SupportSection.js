import React from 'react';

function SupportSection() {
  return (
    <div id="support-section" className="container mt-4">
      <h2>Support</h2>
      <div id="customer-service" className="mb-4">
        <h3>Customer Service</h3>
        <p>For assistance, please reach out to our customer service team.</p>
        <button className="btn btn-primary">Contact Support</button>
      </div>

      <div id="finance-support" className="mb-4">
        <h3>Finance Support</h3>
        <p>If you need assistance with payments or billing, please contact our finance team.</p>
        <button className="btn btn-primary">Contact Finance</button>
      </div>

      <div id="supplier-support" className="mb-4">
        <h3>Supplier Support</h3>
        <p>If you are a supplier and need assistance, please reach out to the supplier support team.</p>
        <button className="btn btn-primary">Contact Supplier</button>
      </div>

      <div id="lawyer-support" className="mb-4">
        <h3>Lawyer Support</h3>
        <p>For legal matters, please contact our legal department.</p>
        <button className="btn btn-primary">Contact Lawyer</button>
      </div>
    </div>
  );
}

export default SupportSection;
