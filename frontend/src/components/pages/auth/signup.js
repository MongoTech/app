import React from 'react';
import { Link } from 'react-router-dom';
import Google from "../../Googel";

export default function Signup({refName, refEmail, refPassword, refPassword2, submitHandler}) {
  return (
    <>
      <div className="vh-100 d-flex justify-content-center">
        <div className="form-access my-auto">
          <form onSubmit={submitHandler}>
            <span>Create Account</span>
            <div className="form-group">
              <input
                type="text"
                className="form-control"
                placeholder="Full Name"
                required
                ref={refName}
              />
            </div>
            <div className="form-group">
              <input
                type="email"
                className="form-control"
                placeholder="Email Address"
                required
                ref={refEmail}
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                className="form-control"
                placeholder="Password"
                required
                ref={refPassword}
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                className="form-control"
                placeholder="Confirm Password"
                required
                ref={refPassword2}
              />
            </div>
            <Google />
            {/*<div className="custom-control custom-checkbox">*/}
            {/*  <input*/}
            {/*    type="checkbox"*/}
            {/*    className="custom-control-input"*/}
            {/*    id="form-checkbox"*/}
            {/*    required*/}
            {/*  />*/}
            {/*  <label className="custom-control-label" htmlFor="form-checkbox">*/}
            {/*    I agree to the{' '}*/}
            {/*    <Link to="/terms-and-conditions">Terms & Conditions</Link>*/}
            {/*  </label>*/}
            {/*</div>*/}
            <button type="submit" className="btn btn-primary">
              Create Account
            </button>
          </form>
          <h2>
            Already have an account?
            <Link to="/login"> Sign in here</Link>
          </h2>
        </div>
      </div>
    </>
  );
}
