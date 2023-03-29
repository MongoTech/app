import React from 'react';
import Google from "../../Googel";

export default function LoginPage({refUsername, refPassword, submitHandler}) {
    return (
        <>
            <div className="vh-100 d-flex justify-content-center">
                <div className="form-access my-auto">
                    <form onSubmit={submitHandler} method="POST">
                        <span>Sign In</span>
                        <div className="form-group">
                            <input
                                ref={refUsername}
                                type="email"
                                name="username"
                                className="form-control"
                                placeholder="Email Address"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <input
                                ref={refPassword}
                                type="password"
                                name="password"
                                className="form-control"
                                placeholder="Password"
                                required
                            />
                        </div>
                        <div>
                        <Google />
                            </div>
                        <button type="submit" className="btn btn-primary">
                            Sign In
                        </button>
                    </form>
                    <h2>
                        If you do not have account please <a href="/signup">Signup</a> password?
                    </h2>
                    <h2>
                        <a href="/forgot">Forgot</a> password?
                    </h2>
                </div>
            </div>
        </>
    );
}
