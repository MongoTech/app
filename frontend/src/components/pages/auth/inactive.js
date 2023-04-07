import React from "react";

export default function Inactive({submitHandler}) {
    return <>   <div className="vh-100 d-flex justify-content-center">
                <div className="form-access my-auto">
                    <form  method="POST" onSubmit={submitHandler}>
                        <span>Activate account</span>
                        <p>You need activate your account, please click button in email, if you don't recive email you can resend it</p>
                        <button type="submit" className="btn btn-primary">
                            Resend
                        </button>
                    </form>

                </div>
            </div></>
}