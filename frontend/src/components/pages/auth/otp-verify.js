import React from 'react';

export default function otpVerify() {
  return (
    <>
      <div className="vh-100 d-flex justify-content-center">
        <div className="form-access my-auto">
          <form>
            <span className="mb-0">OTP Verification</span>
            <p className="text-center mb-4">
              One time code send on on your number
            </p>
            <input
              type="text"
              className="form-control"
              placeholder="Enter code here"
              required
            />
            <button type="submit" className="btn btn-primary">
              Reset
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
