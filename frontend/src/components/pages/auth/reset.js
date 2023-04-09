import React from 'react';
import { Link } from 'react-router-dom';

export default function Reset({refPassword, refPassword2, submitHandler}) {
  return (
    <>
      <div className="vh-100 d-flex justify-content-center">
        <div className="form-access my-auto">
          <form onSubmit={submitHandler}>
            <span>Reset password</span>
            <input
              type="text"
              className="form-control"
              placeholder="Enter Your password"
              required
              ref={refPassword}
            /><br />
              <input
              type="text"
              className="form-control"
              placeholder="Enter Your password again"
              required
              ref={refPassword2}
            />
            <button type="submit" className="btn btn-primary">
              Change password
            </button>

          </form>
        </div>
      </div>
    </>
  );
}
