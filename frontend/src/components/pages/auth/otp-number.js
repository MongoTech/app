import React from 'react';
import { Link } from 'react-router-dom';

export default function otpVerify() {
  return (
    <>
      <div className="vh-100 d-flex justify-content-center">
        <div className="form-access my-auto">
          <form>
            <span className="mb-0">OTP Verification</span>
            <p className="text-center mb-4">
              We will send one time code on this number
            </p>
            <input
              type="phone"
              className="form-control"
              placeholder="Enter your phone number"
              required
            />
            <button type="submit" className="btn btn-primary">
              Send
            </button>
            <h2>
              Don't get code? <Link to="#">Resend</Link>
            </h2>
          </form>
        </div>
      </div>
    </>
  );
}
