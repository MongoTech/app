import React from "react";

export default function From({
                                 title,
                                 button,
                                 submitHandle,
                                 refUsername,
                                 refEmail,
                                 refPassword,
                                 refSuperuser,
                                 refActive,
                                 refLabel,
                                 handleOnChange
                             }) {
    return (
        <><h3>{title}</h3>
            <div className="container-fluid">
                <div className="card">
                    <div className="card-body">
                        <form onSubmit={submitHandle}>
                            <div className="form-row mt-4">
                                <div className="col-md-6">
                                    <label htmlFor="formFirst">Full Name</label>
                                    <input
                                        ref={refUsername}
                                        id="formFirst"
                                        type="text"
                                        className="form-control"
                                        placeholder="First name"
                                    />
                                    <label htmlFor="formLast">Email</label>
                                    <input
                                        ref={refEmail}
                                        id="formFirst"
                                        type="email"
                                        className="form-control"
                                        placeholder="First name"
                                    />
                                    <label htmlFor="formLast">Password</label>
                                    <input
                                        ref={refPassword}
                                        id="formFirst"
                                        type="password"
                                        className="form-control"
                                        placeholder="Password"
                                    />
                                    <div className="form-check">
                                        <input
                                            ref={refSuperuser}
                                            id="isSuperuser"
                                            type="checkbox"
                                            className="form-check-input"
                                        />
                                        <label htmlFor="isSuperuser" className="form-check-label">Is
                                            Superuser</label>
                                    </div>
                                    <div className="form-check">
                                        <input
                                            ref={refActive}
                                            id="isActive"
                                            type="checkbox"
                                            className="form-check-input"
                                        />
                                        <label htmlFor="isActive" className="form-check-label">Is Active</label>
                                    </div>
                                </div>

                                <div className="col-md-12">
                                    <input type="submit" value={button} className="btn btn-primary"/>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </>
    );
}