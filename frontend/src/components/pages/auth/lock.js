import React from 'react';
import { Link } from 'react-router-dom';

export default function otpVerify() {
  return (
    <>
      <div className="vh-100 d-flex justify-content-center">
        <div className="form-access my-auto">
          <form>
            <span>Locked</span>
            <input
              type="password"
              className="form-control"
              placeholder="Enter your password"
              required
            />
            <button type="submit" className="btn btn-primary">
              Unlock
            </button>
            <h2>
              No luck? <Link to="/reset">Reset Password</Link>
            </h2>
          </form>
        </div>
      </div>
    </>
  );
}
